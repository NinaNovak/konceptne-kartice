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
# FUNKCIJE ZA INTERAKTIVNE BLIŽNJICE
# - klik na srečo - glas ljudstva - oblak ključnih besed - ravno prišlo -
##############################################################################
def izberi_nakljucno_kartico():
    '''Vrne ime datoteke naključno izbrane kartice'''
    seznam_imen_datotek = modeli.vrni_imena_datotek_vseh_kartic()
    ime_PDF_datoteke = random.choice(seznam_imen_datotek)
    return ime_PDF_datoteke

def zadnja_dodana():
    '''Vrne ime PDF datoteke naključno izbrane kartice'''
    ime = modeli.ime_pdf_datoteke_zadnje_dodane_kartice()
    return ime

def tabela_v_seznam():
    """Tabelo ključnih besed in števila njihovih pojavitev spremeni v seznam
        seznamov-dvojic.

    """
    #Dobi tabelo vseh ključnih besed in števila njihovih pojavitev.
    oblak = modeli.oblak()
    i = 0
    sez=[]
    for vrstica in oblak:
        sez.append([oblak[i][0], oblak[i][1]])
        i+=1
    return sez
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
    naj_jezik = 'zadnja.png'
    kljucne = 'oblak_kljucnih.png'
    kliknasreco = 'klik_na_sreco.png'
    
    favicon = 'favicon.ico'

    dashboard_css = 'dashboard.css'

    if id_jezika == '':
        #vrni vse konceptne (SKORAJ ISTA KODA 1/2)
        return template('dash',
                        orodja=modeli.nastej_orodja(),#za levi menu
                        kartice=modeli.vrni_tabelo_konceptnih(),#baza kartic
                        
                        #ikone:
                        naj_kartica=naj_kartica,
                        naj_jezik=naj_jezik,
                        kljucne=kljucne,
                        kliknasreco=kliknasreco,
                        
                        favicon = favicon,

                        dashboard_css = dashboard_css,
                        
                        #interaktivne bližnjice
                        nakljucna=izberi_nakljucno_kartico(),
                        zadnja=zadnja_dodana(),
                        max_ogledov=modeli.max_ogledov(),

                        katere="")#ali tabela za vse jezike ali samo za enega
    else:
        #vrni samo konceptne za 1 izbrani jezik (SKORAJ ISTA KODA 2/2)
        return template('dash',
                        orodja=modeli.nastej_orodja(),#za levi menu
                        kartice=modeli.vrni_konceptne_po_jezikih(id_jezika),#baza kartic
                        
                        #ikone:
                        naj_kartica=naj_kartica,
                        naj_jezik=naj_jezik,
                        kljucne=kljucne,
                        kliknasreco=kliknasreco,

                        favicon = favicon,
                        
                        #interaktivne bližnjice
                        nakljucna=izberi_nakljucno_kartico(),
                        zadnja=zadnja_dodana(),
                        max_ogledov=modeli.max_ogledov(),

                        #ali tabela za vse jezike ali samo za enega:
                        katere=" za " + modeli.vrni_ime_orodja(id_jezika))

@route('/ikone/<ikona>')
def serve_icons(ikona):
    return static_file(ikona, root='ikone')
##############################################################################
# DOWNLOAD KARTICE (ogled PDF-ja)
##############################################################################
@route('/kartice/<ime_datoteke>')
def snemanje_kartice(ime_datoteke):
    if (ime_datoteke[-4:] == '.pdf' or ime_datoteke[-4:] == '.PDF'):
        modeli.ogled(ime_datoteke) #poveča število ogledov kartice za 1
    return static_file(ime_datoteke, root='./kartice')
##############################################################################
# TAG CLOUD
##############################################################################
@route('/oblak')
def oblak():
    favicon = 'favicon.ico'
    return template('tags',

                    favicon = favicon,
                    
                    orodja=modeli.nastej_orodja(),#za levi menu
                    oznake=modeli.oblak()
                    )
##############################################################################
# ISKALNIK PO ZBIRKI
##############################################################################
@post('/dashboard')
def iskanje():
    favicon = 'favicon.ico'
    naj_kartica = 'najbolj_priljubljen_jezik.png'
    naj_jezik = 'zadnja.png'
    kljucne = 'oblak_kljucnih.png'
    kliknasreco = 'klik_na_sreco.png'
    niz_iskanje = request.forms.get('iskanje')
    #dodaj iskalni niz v datoteko oziroma povečaj njegovo število iskanj
    seznam_besed = re.findall(r"[\w']+", niz_iskanje)
    try:
        kartice = modeli.vrni_konceptne_rezultat_iskanja(seznam_besed)
    except:
        kartice = modeli.vrni_tabelo_konceptnih_izjema()
    return template('dash',
                    orodja=modeli.nastej_orodja(),#za levi menu
                    kartice=kartice,#baza kartic - rezultat iskanja
                    
                    #ikone
                    favicon = favicon,
                    naj_kartica=naj_kartica,
                    naj_jezik=naj_jezik,
                    kljucne=kljucne,
                    kliknasreco=kliknasreco,

                    #interaktivne bližnjice
                    nakljucna=izberi_nakljucno_kartico(),
                    zadnja=zadnja_dodana(),
                    max_ogledov=modeli.max_ogledov(),
                    
                    katere=" za iskalni niz: " + niz_iskanje)
##############################################################################
# POPRAVLJANJE OBSTOJECE KARTICE
##############################################################################

##############################################################################
# Preden posodobitev izvedemo, mora uporabnik potrditi popravke.
##############################################################################

@route('/uredi_obstojeco')
def obstojeca():

    favicon = 'favicon.ico'
    
    try:
        id_kartice = request.query.id_kartice
    except:
        id_kartice = ''
    return template('uredi_obstojeco',

                    favicon = favicon,
                    
                    orodja=modeli.nastej_orodja(),
                    orodj=modeli.orodja_od_1_kartice(id_kartice),
                    idkartice=id_kartice,
                    kartice=modeli.vrni_eno_kartico(id_kartice),
                    kljucne=modeli.vrni_sez_kljucnih_za_eno_kartico(id_kartice),
                    opis=modeli.vrni_opis_kartice(id_kartice)
                    
                    )
@route('/uredi_obstojeco', method='POST')
def popravi_obstojeco():
    '''Vsa popravila se nanašajo na kartico z ID-jem id_kartice.'''
    try:
        id_kartice = request.query.id_kartice
    except:
        id_kartice = ''#če id='' ... kaj potem?
    ##########################################################################
    #1. spreminjanje naslova kartice
    ##########################################################################
    novo_ime = request.forms.get('ime_kartice')
    if novo_ime != '':
        modeli.spremeni_naslov(id_kartice, novo_ime)
    ##########################################################################
    #2. spreminjanje kratkega opisa
    ##########################################################################
    novi_opis = request.forms.get('opis')
    if novi_opis != '':
        modeli.spremeni_opis(id_kartice, novi_opis)
    ##########################################################################
    #3. spremeni ključne besede
    ##########################################################################
    ##request.forms.getlist('nov_sez_kljucnih')
    ##DA request.forms.get('nove_kljucne')
    #### dodaj  ##############################################################
    nove_kljucne_niz = request.forms.get('nove_kljucne')

    ##
    kljucne = locevanje_kljucnih_besed(nove_kljucne_niz)
    #preveri ponavljanje vnesenih besed
    sez = []
    for beseda in kljucne:
        if beseda not in sez:
            sez.append(beseda)
    kljucne = sez  #shranimo nov seznam, v katerem preverjeno ni ponavljanja
    ##
    
    #dodaj kljucne v bazo, povezi kartico s temi kljucnimi
    modeli.kartica_ima_kljucne(id_kartice, kljucne)
    #### odvzemi #############################################################
    novi_sez = request.forms.getlist('nov_sez_kljucnih')
    stari_sez = vrni_sez_kljucnih_za_eno_kartico(id_kartice)
    odvzete = []
    for kljucna in stari_sez:
        if kljucna not in novi_sez:
            odvzete.appent(kljucna)
    for kljucna in odvzete:
        id_kljucne = modeli.id_kljucne_besede(kljucna)
        modeli.odvzemi_kljucno(id_kartice, id_kljucne)
    ##########################################################################
    #4. orodja
    ##########################################################################
    obkljukana_orodja = request.forms.getlist('stara_orodja')

    #### dodaj orodja ################################################
    #popolnoma novo orodje
    vneseno_or = request.forms.get('nova_orodja')

    ##
    kljucne = locevanje_kljucnih_besed(nove_kljucne_niz)
    #preveri ponavljanje vnesenih besed
    sez = []
    for beseda in kljucne:
        if beseda not in sez:
            sez.append(beseda)
    kljucne = sez  #shranimo nov seznam, v katerem preverjeno ni ponavljanja
    ##
    
    #dodaj kljucne v bazo, povezi kartico s temi kljucnimi
    modeli.kartica_ima_kljucne(id_kartice, kljucne)
    #### odvzemi orodja ##############################################
    stara_or = orodja_od_1_kartice(id_kartice)[0][0]
    ##########################################################################
    #5. nova PDF datoteka
    ##########################################################################
    try:
        request.files.get('nalozi_pdf')
    except:
        None
    ##########################################################################
    #6. nova DOCX datoteka
    ##########################################################################
    try:
        request.files.get('nalozi_docx')
    except:
        None
##############################################################################
# NALAGANJE NOVE KARTICE
##############################################################################

##############################################################################
# = TRANSAKCIJA
##############################################################################

@route('/nalozi_novo_kartico')
def upload():
    favicon = 'favicon.ico'
    return template('upload',

                    favicon = favicon,
                    
                    orodja=modeli.nastej_orodja())

def shranjevanje_PDF(dat):
    nalozena_datoteka = request.files.get(dat)
    name, ext = os.path.splitext(nalozena_datoteka.filename)
    if ext != '.pdf':
        return 'Nedovoljena vrsta datoteke.\nDovoljena vrsta datoteke je PDF.'
    save_path = os.getcwd() + '/kartice'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path,
                                       file=nalozena_datoteka.filename)
    if not os.path.exists(file_path):
        nalozena_datoteka.save(file_path)
    else:
        return 'Datoteka s tem imenom že obstaja.'
def shranjevanje_DOCX(dat):
    nalozena_datoteka_docx = request.files.get(dat)
    save_path_docx = os.getcwd() + '/kartice'
    if not os.path.exists(save_path_docx):
        os.makedirs(save_path_docx)
    file_path_docx = "{path}/{file}".format(path=save_path_docx,
                                            file=nalozena_datoteka_docx.filename)
    if not os.path.exists(file_path_docx):
        nalozena_datoteka_docx.save(file_path_docx)
    else:
        return 'Datoteka s tem imenom že obstaja.'


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
    shranjevanje_PDF('nalozi_pdf')
    ##DOCX oziroma katerakoli datoteka za popravljanje (AI, TEX, ...)
    shranjevanje_DOCX('nalozi_docx')
    ##########################################################################
    #2. dodaj kartico v bazo
    ##########################################################################
    #dobi ime in kratek opis kartice
    ime_kartice = request.forms.get('ime_kartice')
    nalozena_datoteka_docx = request.files.get('nalozi_docx')
    nalozena_datoteka = request.files.get('nalozi_pdf')
    kratek_opis = request.forms.get('opis')
    #dodaj kartico
    modeli.dodaj_kartico(ime_kartice,
                         nalozena_datoteka_docx.filename,#dat za popravljanje
                         nalozena_datoteka.filename,#pdf datoteka
                         kratek_opis)
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
    #dobi id kartice, ki jo dodajamo
    id_kartice = modeli.id_zadnje_dodane_kartice()[0]
    #dodaj kljucne v bazo, povezi kartico s temi kljucnimi
    modeli.kartica_ima_kljucne(id_kartice, kljucne)
    ##########################################################################
    #4. orodje ali programski jezik
    ##########################################################################

    #orodja, ki jih uporabnik odkljuka v seznamu:
    sez_ID_orodij = request.forms.getlist('orodje')
    #vnesi v povezovalno tabelo:
    modeli.kartica_uci_programsko_orodje_jezik(id_kartice, sez_ID_orodij)
    
    #če uporabnik vnese novo orodje:
    novo_orodje = request.forms.get('novo')
    if novo_orodje != '':
        #najprej preveri, da tega orodja še ni v bazi:
        orodja = modeli.nastej_orodja()
        seznam_imen_orodij = []
        for o in orodja:#o...each row
            seznam_imen_orodij.append(o[1])
            
        #če orodja ni v bazi:
        if novo_orodje not in seznam_imen_orodij:
            modeli.dodaj_orodje(novo_orodje)
            id_novega = modeli.id_zadnjega_dodanega_orodja()
            modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                       [id_novega])
        #če orodje je v bazi:
        else:
            #poiscemo ID orodja
            pos = seznam_imen_vseh_orodij.index(novo_orodje)
            id_orodja = orodja[pos][0]
            #uporabnik ga ni odkljukal
            if id_orodja not in sez_ID_orodij:
                modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                           [id_orodja])
            
    ##########################################################################
    #5. pripravimo besedilo za izpis uporabniku
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
           'Kratek opis: <b>{0}</b><br>'.format(kratek_opis)+\
           'Hvala!</br></br>' +\
           '<a href="dashboard">Nazaj na prvo stran</a>'
##############################################################################
# O STRANI
##############################################################################
@route('/o_strani')
def o_strani():
    favicon = 'favicon.ico'
    return template('o_strani',
                    favicon = favicon,                    
                    orodja=modeli.nastej_orodja())
###############
run(debug=True)
##############################################################################
# THE END
##############################################################################
##############################################################################
# ZBRIŠI
##############################################################################
#TIRALICA = najveckrat iskano geslo
#ta izbira vrne: 1) podatek: najveckrat iskano geslo in
#                2) tabelo konceptnih, ki vsebujejo to geslo
#                basically: rezultat search-a za najbolj iskano geslo + na
#        vrhu izpis: Največkrat iskano geslo na tej spletni strani je: "xxxxx"
#-----------------------------------------------------------------------------
#Vsako iskano geslo, ki ga kdo vnese v search, zabeležim v tekstovno datoteko
#najveckrat_iskano_geslo.txt. Če je geslo že v datoteki, povečam števec.
@route('/tiralica')
def tiralica():
    maks = 2#največje število iskanj
            #začetna vrednost maks je 2, ker nas zanimajo samo besede, ki so bile iskane vsaj 2-krat
    geslo = []#maks-krat iskanih je bilo lahko več gesel
    
    dat = open('najveckrat_iskano_geslo.txt', 'r')
    a = dat.readlines()#seznam vrstic
    #do tuki dela
    #dat.close()
    
    if len(a) == 0:#če je datoteka prazna?
        rezultat="Nobeno geslo ni bilo iskano več kot enkrat."
        return template('tiralica',
                            orodja=modeli.nastej_orodja(),#za levi menu
                            rezultat=rezultat
                            )
    for i in range(len(a) - 1):#zadnja vrstica ne vsebuje \n
        a[i] = a[i][:-1]#[:-1] odreže \n
        #if i == -1:#moramo shraniti a[-2], ker drugače ob preverjanju zadnjega elementa ni dostopen?
            
        try:
            a[i] = int(a[i])
            st_iskanj=int(a[i])
            if st_iskanj == maks:
                geslo = geslo.append(a[i - 1])#vsaka druga vrstica je število iskanj. geslo, za katerega velja število iskanj, je zapisano v vrstici pred njo.
            elif st_iskanj > maks:
                maks = st_iskanj
                geslo = [a[i - 1]]
        except:
            continue

    ###zadnji element seznama posebej, ker nima \n
    try:
        a[-1] = int(a[-1])
        st_iskanj=a[-1]
        if st_iskanj == maks:
            geslo.append(a[-2])#vsaka druga vrstica je število iskanj. geslo, za katerega velja število iskanj, je zapisano v vrstici pred njo.
        elif st_iskanj > maks:
            maks = st_iskanj
            geslo = [a[-2]]
        m = 'zadnji try do konca izveden'
    except:
        m = 'zadnji try je bil except'
    ###

    if geslo == []:
        rezultat="Nobeno geslo ni bilo iskano več kot enkrat."
    elif len(geslo) == 1:
        rezultat="Največkrat iskano geslo je " + geslo[0] + ". Iskano je bilo " + str(maks) + "-krat."
    elif len(geslo) == 2:#dvojina:)
        gesla = ", ".join(geslo)
        rezultat = "Največkrat iskani gesli sta: " + gesla + ". Vsakega so iskali " + str(maks) + "-krat."
    else:
        gesla = ", ".join(geslo)
        rezultat = "Največkrat iskana gesla so: " + gesla + ". Vsakega so iskali " + str(maks) + "-krat."

    favicon = 'favicon.ico'
    return template('tiralica',
                    favicon = favicon,
                    orodja=modeli.nastej_orodja(),#za levi menu
                    rezultat=rezultat
                    )
##############################################################################
# IGRIŠČE
##############################################################################
@route('/igrisce')
def igrisce():

    naj_kartica = 'najbolj_priljubljen_jezik.png'
    naj_jezik = 'zadnja.png'
    kljucne = 'oblak_kljucnih.png'
    kliknasreco = 'klik_na_sreco.png'

    favicon = 'favicon.ico'
    
    return template('igrisce',

                    #ikone:
                    naj_kartica=naj_kartica,
                    naj_jezik=naj_jezik,
                    kljucne=kljucne,
                    kliknasreco=kliknasreco,

                    favicon = favicon,
                    
                    orodja=modeli.nastej_orodja())
##@route('/uredi_obstojeco', method='POST')
##def popravi_obstojeco():
##    '''TRANSAKCIJA'''
##    #modeli.transakcija(...)
##    '''TRY-CATCH blok:
##TRY - dobimo sporočilo z vnešenimi podatki
##CATCH - dobimo sporočilo 'nepričakovana napaka'
##
##    '''
##    ##########################################################################
##    #1. shrani datoteko na disk
##    ##########################################################################
##    ##PDF
##    nalozena_datoteka = request.files.get('nalozi_pdf')
##    name, ext = os.path.splitext(nalozena_datoteka.filename)
##    if ext != '.pdf':
##        return 'Nedovoljena vrsta datoteke.\nDovoljena vrsta datoteke je PDF.'
##    save_path = os.getcwd() + '/kartice'
##    if not os.path.exists(save_path):
##        os.makedirs(save_path)
##    file_path = "{path}/{file}".format(path=save_path,
##                                       file=nalozena_datoteka.filename)
##    ##DOCX oziroma katerakoli datoteka za popravljanje (AI, TEX, ...)
##    nalozena_datoteka_docx = request.files.get('nalozi_docx')
##    save_path = os.getcwd() + '/kartice'
##    if not os.path.exists(save_path):
##        os.makedirs(save_path)
##    file_path = "{path}/{file}".format(path=save_path,
##                                       file=nalozena_datoteka_docx.filename)
##    ##
##    
##    #ujemi napako IOError('File exists.') oziroma OSError: File exists.
##    #vrni 'Datoteka s tem imenom že obstaja. Ali jo želite zamenjati?'
##
##
##
##    if not os.path.exists(file_path):
##        nalozena_datoteka.save(file_path)
##    else:
##        return 'Datoteka s tem imenom že obstaja.'
##    #return "Datoteka je bila uspešno shranjena v mapo '{0}'.".format(save_path)
##
##    ##########################################################################
##    #2. dodaj kartico v bazo
##    ##########################################################################
##    #dobi ime in kratek opis kartice
##    ime_kartice = request.forms.get('ime_kartice')
##    kratek_opis = request.forms.get('opis')
##    #dodaj kartico, dobi njen id
##    modeli.dodaj_kartico(ime_kartice,
##                         nalozena_datoteka_docx.filename,#dat za popravljanje
##                         nalozena_datoteka.filename,#pdf datoteka
##                         kratek_opis)
##    id_kartice = modeli.id_zadnje_dodane_kartice()[0]
##
##    ##########################################################################
##    #3. kljucne besede
##    ##########################################################################
##    #dobi ~niz kljucnih, naredi ~seznam kljucnih
##    kljucne_skupaj = request.forms.get('kljucne')
##    kljucne = locevanje_kljucnih_besed(kljucne_skupaj)
##    #preveri ponavljanje vnesenih besed
##    sez = []
##    for beseda in kljucne:
##        if beseda not in sez:
##            sez.append(beseda)
##    kljucne = sez  #shranimo nov seznam, v katerem preverjeno ni ponavljanja
##    #dodaj kljucne v bazo, povezi kartico s temi kljucnimi
##    modeli.kartica_ima_kljucne(id_kartice, kljucne)
##    
##    ##########################################################################
##    #4. orodje ali programski jezik
##    ##########################################################################
##    #dobi seznam orodij, ki jih uci kartica:
##    sez_ID_orodij = request.forms.getlist('orodje')
##    #vnesi v povezovalno tabelo:
##    modeli.kartica_uci_programsko_orodje_jezik(id_kartice, sez_ID_orodij)
##    
##    #novo orodje:
##    novo_orodje = request.forms.get('novo')
##    #ali je uporabnik vnesel novo orodje:
##    if novo_orodje != '':
##        #najprej preveri, ali tega orodja ni v bazi:
##        orodja = modeli.nastej_orodja()
##        seznam_imen_orodij = []
##        for o in orodja:#o...each row
##            seznam_imen_orodij.append(o[1])
##        #orodja ni v bazi
##        if novo_orodje not in seznam_imen_orodij:
##            modeli.dodaj_orodje(novo_orodje)
##            id_novega = modeli.id_zadnjega_dodanega_orodja()
##            modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
##                                                       [id_novega])
##        #orodje je v bazi
##        else:
##            #poiscemo ID orodja
##            pos = seznam_imen_vseh_orodij.index(novo_orodje)
##            id_orodja = orodja[pos][0]
##            #uporabnik ga ni odkljukal
##            if id_orodja not in sez_ID_orodij:
##                modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
##                                                           [id_orodja])
##            
##    ##########################################################################
##    #5. pripravimo orodja in ključne besede za izpis uporabniku
##    ##########################################################################
##    niz_orodje = ''
##    #sez_ID_orodij hrani id-je izbranih orodij, mi potrebujemo imena
##    for id_orodja in sez_ID_orodij:
##        ime = modeli.vrni_ime_orodja(id_orodja)
##        niz_orodje += ime
##        niz_orodje += ', '
##    if novo_orodje != '':
##        niz_orodje += novo_orodje
##    else:
##        niz_orodje = niz_orodje[:-2]
##        
##    niz_kljucne = ''
##    for k in kljucne:
##        niz_kljucne += k
##        niz_kljucne += ', '
##    niz_kljucne = niz_kljucne[:-2]
##    
##    return 'Dodajanje nove kartice je bilo uspešno.<br><br>' +\
##           '<b>Vnešeni podatki</b><br><br>' +\
##           'Ime kartice: <b>{0}</b><br>'.format(ime_kartice) +\
##           'Ime PDF datoteke: <b>{0}</b><br>'.format(nalozena_datoteka.filename) +\
##           'Ime DOCX/DOC datoteke: <b>{0}</b><br>'.format(nalozena_datoteka_docx.filename) +\
##           'Orodja/programski jeziki, ' +\
##           'ki jih uči kartica: <b>{0}</b><br>'.format(niz_orodje) +\
##           'Ključne besede za iskanje ' +\
##           'konceptne kartice: <b>{0}</b><br>'.format(niz_kljucne) +\
##           'Kratek opis: <b>{0}</b><br>'.format(kratek_opis)+\
##           'Hvala!</br></br>' +\
##           '<a href="dashboard">Nazaj na prvo stran</a>'
