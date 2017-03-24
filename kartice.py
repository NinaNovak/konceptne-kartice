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
    Če mapa ime_mape ne obstaja, je ustvajena.

    Datoteke dat je tipa bottle.FileUpload:
    >>> type(dat)
    <class 'bottle.FileUpload'>

    '''
    

@route('/nalozi_novo_kartico')
def upload():
    return template('upload',
                    orodja=modeli.nastej_orodja())

@route('/nalozi_novo_kartico', method='POST')
def do_upload():  #(kako narediti, da bo ta funkcija transakcija?)
    ''''''
    #1. shrani datoteko na disk
    nalozena_datoteka = request.files.get('upload')
    modeli.shrani_pdf_v_blob(nalozena_datoteka)
    name, ext = os.path.splitext(nalozena_datoteka.filename)
    if ext != '.pdf':
        return 'Nedovoljena vrsta datoteke.\nDovoljena vrsta datoteke je PDF.'
    save_path = os.getcwd() + '/pdfkartice'
    ##kot za pdf naredi tudi za docx in ostale wordove koncnice
    ##zato, da se konceptno kartico lahko popravi/spremeni
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

    #2. dodaj kartico v bazo
    #dobi ime kartice
    ime_kartice = request.forms.get('ime_kartice')
    #dodaj kartico, dobi njen id
    modeli.dodaj_kartico(ime_kartice, nalozena_datoteka.filename)
    id_kartice = modeli.id_zadnje_dodane_kartice()

    #3. kljucne besede
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

    #4. orodje ali programski jezik
    #dobi seznam orodij, ki jih uci kartica:
    sez_id_orodij = request.forms.getlist('orodje')
    #vnesi v povezovalno tabelo:
    modeli.kartica_uci_programsko_orodje_jezik(id_kartice, sez_id_orodij)
    
    #novo orodje (če uporabnik izpolni polje 'Drugo'):
    novo_orodje = request.forms.get('novo')
    if novo_orodje != '':
        #vseeno preveri, ali tega orodja ni v bazi:
        vrstica = modeli.nastej_orodja()
        for orodje1 in vrstica:

            #1. Ce je ze v bazi in
            #2. ce ga se ni v povezovalni tabeli,
            #3. ga dodaj v povezovalno tabelo.
            orodje_niz = orodje1[0]
            print('orodje1[0]: '+str(orodje1[0]))
            print('tip orodje1[0]: '+str(type(orodje1[0])))
            if vrstica[0] == novo_orodje:  #orodje ze obstaja
                #PREVERITI, ALI ZE V SEZNAMU orodje?
                id_novega_orodja = vrstica[1]
                modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                           id_novega_orodja)

                #treba je samo vnesti povezavo kartica<--->to_orodje v tabelo
                #kartica_uci_programsko_orodje_jezik

            #1. Orodja ni v bazi,
            #2. zato ga dodaj v tabelo orodja in
            #3. v povezovalno tabelo.
            else:  #orodje se ne obstaja
                modeli.dodaj_orodje(novo_orodje)
                id_novega_orodja = modeli.id_zadnjega_dodanega_orodja()
                
                #vnesi v povezovalno tabelo
                print('imamo ukaz \'orodje.append(novo_orodje)\'.')
                print('tip orodje: '+str(type(orodje)))
                print('tip novo_orodje: '+str(type(novo_orodje)))
                modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                           id_novega_orodja)

    #pripravimo orodja in ključne besede za izpis uporabniku
    niz_orodje = ''
    for o in orodje:
        niz_orodje += o
        niz_orodje += ', '
    niz_orodje = niz_orodje[:-2]
    niz_kljucne = ''
    return 'Dodajanje nove kartice je bilo uspešno.\n\n' +\
           'Vnešeni podatki:\n\n' +\
           'Ime kartice: {0}\n'.format(ime_kartice) +\
           'Ime datoteke: {0}\n'.format(nalozena_datoteka) +\
           'Orodja/programski jeziki, ki jih uči kartica: {0}\n'.format(orodje) +\
           'Ključne besede za iskanje konceptne kartice: {0}\n'.format(kljucne) +\
           'Hvala!\n'

##############################################################################
# 
##############################################################################

run(debug=True)
