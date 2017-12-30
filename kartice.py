from bottle import *
import os
import modeli
import re
import random
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
def vse_kljucne_od_1_kartice(id_kartice):
    kljucne = modeli.vrni_sez_kljucnih_za_eno_kartico(id_kartice)
    return kljucne
##############################################################################
# RAZNO / V DELU
##############################################################################
def oblak_kljucnih_besed():
    #dobi vse ključne besede iz baze
    
    #jih uredi glede na število pojavitev - ali lahko to naredimo v modeli.py?

    #JA:napiše jih kot tekst v vrsti
    #posamezne ključne besede loči z " . "
    #za vsakih 10 pojavitev več je font teksta besede za n pikslov večji -
    #omejitev - največji font je npr 60 pikslov
    #da ne bojo ključne besede v ful dolgi vrsti, širino vrstice omejiti na n znakov
    
    #NE:jih razporedi v krogu...naredi prej jpg?...
    pass

def izberi_nakljucno_kartico():
    '''Vrne ime datoteke naključno izbrane kartice'''
    seznam_imen_datotek = modeli.vrni_imena_datotek_vseh_kartic()
    ime_PDF_datoteke = random.choice(seznam_imen_datotek)
    return ime_PDF_datoteke

#NAJBOLJ PRILJUBLJEN JEZIK = najveckrat iskano geslo
#ta izbira vrne: 1) podatek: najveckrat iskano geslo in
#                2) tabelo konceptnih, ki vsebujejo to geslo
#                basically: rezultat search-a za najbolj iskano geslo + na
#        vrhu izpis: Največkrat iskano geslo na tej spletni strani je: "xxxxx"
#-----------------------------------------------------------------------------
#Vsako iskano geslo, ki ga kdo vnese v search, zabeležim v tekstovno datoteko
#najveckrat_iskano_geslo.txt. Če je geslo že v datoteki, povečam števec.
def najbolj_iskano_geslo():
    '''Prebere tekstovno datoteko najveckrat_iskano_geslo.txt,

    ki se nahaja v trenutni mapi. Vrne najveckrat iskano geslo, to je niz
    iz prve vrstice te datoteke.

    '''
    #če tekstovna datoteka najveckrat_iskano_geslo.txt ne obstaja
    if ...:
        return 'Na tej strani ni še nihče uporabil storitve \'Išči...\'.'
    
    pass

#OBLAK KLJUČNIH BESED = katere vsebine so v bazi?
#ta izbira vrne: v oblak tag-ov oblikovane vse ključne besede, vključno z
#                jeziki!, na tag-e lahko klikneš in dobiš rezultat search-a
#                za ta tag. Glede na pogostost pojavitve tag-a je velikost
#                pisave primerno večja.
#-----------------------------------------------------------------------------
#Iz baze s pomočjo ukaza "PREŠTEJ ŠTEVILO POJAVITEV" (funkcija XXXX iz
#modeli.py) dobim po velikosti urejen seznam vseh ključnih besed in jezikov z
#številom pojavitev.
#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


##############################################################################
# ZBRIŠI
##############################################################################
@route('/index')
def index():
    naj_kartica = 'najbolj_priljubljen_jezik.png'
    naj_jezik = 'tiralica.png'
    kljucne = 'oblak_kljucnih.png'
    kliknasreco = 'klik_na_sreco.png'

    return template('index',
                        naj_kartica=naj_kartica,
                        naj_jezik=naj_jezik,
                        kljucne=kljucne,
                        kliknasreco=kliknasreco)
##############################################################################
# PRVA STRAN
##############################################################################
@route('/dashboard')
def dash():
    ##########################################################################
    # prikaz kartic v tabeli glede na jezike (vse ali za 1 izbrani jezik)
    ##########################################################################
    id_jezika = request.query.id_jezika

    naj_kartica = 'najbolj_priljubljen_jezik.png'
    naj_jezik = 'tiralica.png'
    kljucne = 'oblak_kljucnih.png'
    kliknasreco = 'klik_na_sreco.png'

    if id_jezika == '':
        #vrni vse konceptne (SKORAJ ISTA KODA 1/2)
        return template('dash',
                        orodja=modeli.nastej_orodja(),
                        kartice=modeli.vrni_tabelo_konceptnih(),
                        
                        naj_kartica=naj_kartica,
                        naj_jezik=naj_jezik,
                        kljucne=kljucne,
                        kliknasreco=kliknasreco,
                        
                        nakljucna=izberi_nakljucno_kartico(),
                        najbolj_iskano=najbolj_iskano_geslo(),

                        katere="")
    else:
        #vrni samo konceptne za 1 izbrani jezik (SKORAJ ISTA KODA 2/2)
        return template('dash',
                        orodja=modeli.nastej_orodja(),
                        kartice=modeli.vrni_konceptne_po_jezikih(id_jezika),
                        
                        naj_kartica=naj_kartica,
                        naj_jezik=naj_jezik,
                        kljucne=kljucne,
                        kliknasreco=kliknasreco,

                        nakljucna=izberi_nakljucno_kartico(),

                        katere=" za " + modeli.vrni_ime_orodja(id_jezika))

@route('/ikone/<ikona>')
def serve_icons(ikona):
    return static_file(ikona, root='ikone')

##############################################################################
# DOWNLOAD KARTICE (ogled PDF-ja)
##############################################################################
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
                    kartice=kartice,

                    nakljucna=izberi_nakljucno_kartico())
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
                    orodj=modeli.orodja_od_1_kartice(id_kartice),
                    idkartice=id_kartice,
                    kartice=modeli.vrni_eno_kartico(id_kartice),
                    kljucne=modeli.vrni_sez_kljucnih_za_eno_kartico(id_kartice))







@route('/uredi_obstojeco', method='POST')
def popravi_obstojeco():
    '''TRANSAKCIJA'''
    #modeli.transakcija(...)
    '''TRY-CATCH blok:
TRY - dobimo sporočilo z vnešenimi podatki
CATCH - dobimo sporočilo 'nepričakovana napaka'

    '''
    ##########################################################################
    #1. shrani datoteko na disk
    ##########################################################################
    ##PDF
    nalozena_datoteka = request.files.get('nalozi_pdf')
    name, ext = os.path.splitext(nalozena_datoteka.filename)
    if ext != '.pdf':
        return 'Nedovoljena vrsta datoteke.\nDovoljena vrsta datoteke je PDF.'
    save_path = os.getcwd() + '/kartice'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path,
                                       file=nalozena_datoteka.filename)
    ##DOCX oziroma katerakoli datoteka za popravljanje (AI, TEX, ...)
    nalozena_datoteka_docx = request.files.get('nalozi_docx')
    save_path = os.getcwd() + '/kartice'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path,
                                       file=nalozena_datoteka_docx.filename)
    ##
    
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
    modeli.dodaj_kartico(ime_kartice,
                         nalozena_datoteka_docx.filename,#dat za popravljanje
                         nalozena_datoteka.filename)#pdf datoteka
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
           'Ime PDF datoteke: <b>{0}</b><br>'.format(nalozena_datoteka.filename) +\
           'Ime DOCX/DOC datoteke: <b>{0}</b><br>'.format(nalozena_datoteka_docx.filename) +\
           'Orodja/programski jeziki, ' +\
           'ki jih uči kartica: <b>{0}</b><br>'.format(niz_orodje) +\
           'Ključne besede za iskanje ' +\
           'konceptne kartice: <b>{0}</b><br>'.format(niz_kljucne) +\
           'Hvala!</br></br>' +\
           '<a href="dashboard">Nazaj na prvo stran</a>'














##############################################################################
# NALAGANJE NOVE KARTICE = TRANSAKCIJA
##############################################################################
@route('/nalozi_novo_kartico')
def upload():
    return template('upload',
                    orodja=modeli.nastej_orodja())

@route('/nalozi_novo_kartico', method='POST')
def do_upload():
    '''TRANSAKCIJA'''
    #modeli.transakcija(...)
    '''TRY-CATCH blok:
TRY - dobimo sporočilo z vnešenimi podatki
CATCH - dobimo sporočilo 'nepričakovana napaka'

    '''
    ##########################################################################
    #1. shrani datoteko na disk
    ##########################################################################
    ##PDF
    nalozena_datoteka = request.files.get('nalozi_pdf')
    name, ext = os.path.splitext(nalozena_datoteka.filename)
    if ext != '.pdf':
        return 'Nedovoljena vrsta datoteke.\nDovoljena vrsta datoteke je PDF.'
    save_path = os.getcwd() + '/kartice'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path,
                                       file=nalozena_datoteka.filename)
    ##DOCX oziroma katerakoli datoteka za popravljanje (AI, TEX, ...)
    nalozena_datoteka_docx = request.files.get('nalozi_docx')
    save_path = os.getcwd() + '/kartice'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path,
                                       file=nalozena_datoteka_docx.filename)
    ##
    
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
    modeli.dodaj_kartico(ime_kartice,
                         nalozena_datoteka_docx.filename,#dat za popravljanje
                         nalozena_datoteka.filename)#pdf datoteka
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
           'Ime PDF datoteke: <b>{0}</b><br>'.format(nalozena_datoteka.filename) +\
           'Ime DOCX/DOC datoteke: <b>{0}</b><br>'.format(nalozena_datoteka_docx.filename) +\
           'Orodja/programski jeziki, ' +\
           'ki jih uči kartica: <b>{0}</b><br>'.format(niz_orodje) +\
           'Ključne besede za iskanje ' +\
           'konceptne kartice: <b>{0}</b><br>'.format(niz_kljucne) +\
           'Hvala!</br></br>' +\
           '<a href="dashboard">Nazaj na prvo stran</a>'
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
