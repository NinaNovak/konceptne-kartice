from bottle import *
import os
import modeli
import re
##############################################################################
# POMOŽNE FUNKCIJE
##############################################################################
def kljucne_niz(kart='vse'):
    '''Dobi objekt=seznam kljucnih, vrne objekt=niz kljucnih.'''
    if kart == 'vse':
        kljucne = modeli.vrni_vse_kljucne_besede()
    else:
        kljucne = modeli.vrni_sez_kljucnih_za_eno_kartico(kart)
    niz = ''
    for k in kljucne:
        klj = str(k)
        niz += klj
        niz += ', '
    niz = niz[:-2]
    return niz
def locevanje_kljucnih_besed(niz):
    '''Iz niza z vejico ločenih besed naredi seznam posameznih besed.'''
    locimo = niz.split(',')  #razbijemo na posamezne besede
    for i in range(len(locimo)):  #odstranimo vsem besedam bele znake
        locimo[i] = locimo[i].strip()
    return locimo
##############################################################################
# RAZNO / V DELU
##############################################################################

##############################################################################
# PRVA STRAN
##############################################################################
@route('/dashboard')
def dash():
    ##########################################################################
    # prikaz kartic v tabeli glede na jezike (vse ali za 1 izbrani jezik)
    ##########################################################################
    id_jezika = request.query.id_jezika
    if id_jezika == '':
        #vrni vse konceptne
        return template('dash',
                        orodja=modeli.nastej_orodja(),
                        kartice=modeli.vrni_tabelo_konceptnih())
    else:
        #vrni samo konceptne za 1 izbrani jezik
        return template('dash',
                        orodja=modeli.nastej_orodja(),
                        kartice=modeli.vrni_konceptne_po_jezikih(id_jezika))
##############################################################################
# DOWNLOAD KARTICE (oziroma ogled PDF-ja)
##############################################################################d
@route('/kartice/<ime_datoteke>')
def snemanje_kartice(ime_datoteke):
    return static_file(ime_datoteke, root='./kartice')
##############################################################################
# ISKALNIK PO ZBIRKI
##############################################################################
@post('/dashboard')
def iskanje():
    niz_iskanje = request.forms.get('iskanje')
    seznam_besed = re.findall(r"[\w']+", niz_iskanje)
    try:
        kartice = modeli.vrni_konceptne_rezultat_iskanja(seznam_besed)
    except:
        kartice = modeli.vrni_tabelo_konceptnih_izjema()
    return template('dash',
                    orodja=modeli.nastej_orodja(),
                    kartice=kartice)
##############################################################################
# POPRAVLJANJE OBSTOJECE KARTICE
##############################################################################
@route('/uredi_obstojeco')
def obstojeca():
    try:
        id_kartice = request.query.id_kartice
    except:
        id_kartice = ''
    return template('uredi_obstojeco',
                    orodja=modeli.nastej_orodja(),
                    idkartice=id_kartice,
                    kartice=modeli.vrni_eno_kartico(id_kartice))

@route('/uredi_obstojeco', method='POST')
def popravi_obstojeco():
    pass
##############################################################################
# NALAGANJE NOVE KARTICE
##############################################################################
@route('/nalozi_novo_kartico')
def upload():
    return template('upload',
                    orodja=modeli.nastej_orodja())

@route('/nalozi_novo_kartico', method='POST')
def do_upload():  #ni transakcija?
    ''''''
    ##########################################################################
    #1. shrani datoteko na disk
    ##########################################################################
    nalozena_datoteka = request.files.get('upload')
    name, ext = os.path.splitext(nalozena_datoteka.filename)
    if ext != '.pdf':
        return 'Nedovoljena vrsta datoteke.\nDovoljena vrsta datoteke je PDF.'
    save_path = os.getcwd() + '/kartice'
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
    sez_ID_orodij = request.forms.getlist('orodje')
    #vnesi v povezovalno tabelo:
    modeli.kartica_uci_programsko_orodje_jezik(id_kartice, sez_ID_orodij)
    
    #novo orodje:
    novo_orodje = request.forms.get('novo')
    #ali je uporabnik vnesel novo orodje:
    if novo_orodje != '':
        #najprej preveri, ali tega orodja ni v bazi:
        orodja = modeli.nastej_orodja()
        seznam_imen_orodij = []
        for o in orodja:#o...each row
            seznam_imen_orodij.append(o[1])
        #orodja ni v bazi
        if novo_orodje not in seznam_imen_orodij:
            modeli.dodaj_orodje(novo_orodje)
            id_novega = modeli.id_zadnjega_dodanega_orodja()
            modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                       [id_novega])
        #orodje je v bazi
        else:
            #poiscemo ID orodja
            pos = seznam_imen_vseh_orodij.index(novo_orodje)
            id_orodja = orodja[pos][0]
            #uporabnik ga ni odkljukal
            if id_orodja not in sez_ID_orodij:
                modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                           [id_orodja])
            
    ##########################################################################
    #5. pripravimo orodja in ključne besede za izpis uporabniku
    ##########################################################################
    niz_orodje = ''
    #sez_ID_orodij hrani id-je izbranih orodij, mi potrebujemo imena
    for id_orodja in sez_ID_orodij:
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
# O STRANI
##############################################################################
@route('/o_strani')
def o_strani():
    return template('o_strani',
                    orodja=modeli.nastej_orodja())
###############
run(debug=True)
##############################################################################
# THE END
##############################################################################
