from bottle import *
import os
import modeli

##############################################################################
# NALAGANJE NOVE KARTICE
##############################################################################

def locevanje_kljucnih_besed(niz):
    '''Iz niza z vejico ločenih besed naredi seznam posameznih besed.'''
    locimo = niz.split(',')  #razbijemo na posamezne besede
    for i in range(len(locimo)):  #odstranimo vsem besedam bele znake
        locimo[i] = locimo[i].strip()
    return locimo

def shranjevanje_datoteke_na_disk(dat, ime_mape):
    '''Datoteko, dobljeno z request.files.get(dat), shrani v mapo ime_mape.

    Mapa ime_mape je v isti mapi kot ta .py datoteka.
    Če mapa ime_mape ne obstaja, je ustvarjena.

    Datoteke dat je tipa bottle.FileUpload:
    >>> type(dat)
    <class 'bottle.FileUpload'>

    '''

##@route('/static/<filepath:path>')
##def server_static(filepath):
##    return static_file(filepath, root='/')

@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='views/')

@route('/dashboard')
def dash():
    return template('dash',
                    orodja=modeli.nastej_orodja())
    
@get('/popravi_kartico/<id_kartice>')
def popravljanje(id_kartice):
    return template('popravi',
                    kartica=modeli.vrni_kartico(id_kartice))

@route('/kartica/<id_kartice>')
def pokazi_pdf(id_kartice):
    pass

def kljucne_niz():
    '''Dobi objekt=seznam kljucnih, vrne objekt=niz kljucnih.'''
    kljucne = modeli.vrni_vse_kljucne_besede()
    niz = '"'
    for k in kljucne:
        klj = str(k)
        niz += klj
        niz += '", "'
    niz = niz[:-3]
    return niz

@route('/vse')
def vse():
    return template('vse',
                    kljucne=kljucne_niz(),
                    kartice=modeli.vrni_tabelo_konceptnih())

@route('/nalozi_novo_kartico')
def upload():
    return template('upload',
                    orodja=modeli.nastej_orodja())

@route('/nalozi_novo_kartico', method='POST')
def do_upload():  #(kako narediti, da bo ta funkcija transakcija?)
    ''''''
    ##########################################################################
    #1. shrani datoteko na disk
    ##########################################################################
    nalozena_datoteka = request.files.get('upload')
    modeli.shrani_pdf_v_blob(nalozena_datoteka)
    name, ext = os.path.splitext(nalozena_datoteka.filename)
    if ext != '.pdf':
        return 'Nedovoljena vrsta datoteke.\nDovoljena vrsta datoteke je PDF.'
    save_path = os.getcwd() + '/pdfkartice'
    ##kot za pdf naredi tudi za docx in ostale wordove koncnice
    ##zato, da se konceptno kartico lahko popravlja/spreminja
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path,
                                       file=nalozena_datoteka.filename)
    #ujemi napako IOError('File exists.') oziroma OSError: File exists.
    #vrni 'Datoteka s tem imenom že obstaja. Ali jo želite zamenjati?'
    if not os.path.exists(file_path):
        nalozena_datoteka.save(file_path)
    else:
        return 'Datoteka s tem imenom že obstaja.'
    #return "Datoteka je bila uspešno shranjena v mapo '{0}'.".format(save_path)

    ##########################################################################
    #2. dodaj kartico v bazo
    ##########################################################################
    #dobi ime kartice
    ime_kartice = request.forms.get('ime_kartice')
    #dodaj kartico, dobi njen id
    modeli.dodaj_kartico(ime_kartice, nalozena_datoteka.filename)
    id_kartice = modeli.id_zadnje_dodane_kartice()[0]

    ##########################################################################
    #3. kljucne besede
    ##########################################################################
    #dobi ~niz kljucnih, naredi ~seznam kljucnih
    kljucne_skupaj = request.forms.get('kljucne')
    kljucne = locevanje_kljucnih_besed(kljucne_skupaj)
    #preveri ponavljanje vnesenih besed
    sez = []
    for beseda in kljucne:
        if beseda not in sez:
            sez.append(beseda)
    kljucne = sez  #shranimo nov seznam, v katerem preverjeno ni ponavljanja
    #dodaj kljucne v bazo, povezi kartico s temi kljucnimi
    modeli.kartica_ima_kljucne(id_kartice, kljucne)
    
    ##########################################################################
    #4. orodje ali programski jezik
    ##########################################################################
    #dobi seznam orodij, ki jih uci kartica:
    sez_orodij = request.forms.getlist('orodje')
    #vnesi v povezovalno tabelo:
    modeli.kartica_uci_programsko_orodje_jezik(id_kartice, sez_orodij)
    
    #novo orodje:
    novo_orodje = request.forms.get('novo')
    #ali je uporabnik vnesel novo orodje:
    if novo_orodje != '':
        #najprej preveri, ali tega orodja ni v bazi:
        orodja = modeli.nastej_orodja()
        #orodja ni v bazi
        if novo_orodje not in orodja[1]:
            modeli.dodaj_orodje(novo_orodje)
            id_novega = modeli.id_zadnjega_dodanega_orodja()
            modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                       [id_novega])
        #orodje je v bazi
        else:
            #uporabnik ga ni odkljukal
            if id_orodja not in sez_orodij:
                modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                           [id_orodja])
            
    ##########################################################################
    #5. pripravimo orodja in ključne besede za izpis uporabniku
    ##########################################################################
    niz_orodje = ''
    #sez_orodij hrani id-je izbranih orodij, mi potrebujemo imena
    for id_orodja in sez_orodij:
        ime = modeli.vrni_ime_orodja(id_orodja)
        niz_orodje += ime
        niz_orodje += ', '
    if novo_orodje != '':
        niz_orodje += novo_orodje
    else:
        niz_orodje = niz_orodje[:-2]
        
    niz_kljucne = ''
    for k in kljucne:
        niz_kljucne += k
        niz_kljucne += ', '
    niz_kljucne = niz_kljucne[:-2]
    
    return 'Dodajanje nove kartice je bilo uspešno.<br><br>' +\
           '<b>Vnešeni podatki</b><br><br>' +\
           'Ime kartice: <b>{0}</b><br>'.format(ime_kartice) +\
           'Ime datoteke: <b>{0}</b><br>'.format(nalozena_datoteka.filename) +\
           'Orodja/programski jeziki, ' +\
           'ki jih uči kartica: <b>{0}</b><br>'.format(niz_orodje) +\
           'Ključne besede za iskanje ' +\
           'konceptne kartice: <b>{0}</b><br>'.format(niz_kljucne) +\
           'Hvala!'

##############################################################################
# 
##############################################################################

run(debug=True)
