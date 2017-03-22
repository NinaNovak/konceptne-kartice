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

    #2. dobi: ime kartice; orodje, ki ga kartica uči; ključne besede;
    ime_kartice = request.forms.get('ime_kartice')

    # dodaj kartico, dobi njen id
    modeli.dodaj_kartico(ime_kartice, nalozena_datoteka.filename)
    id_kartice = modeli.id_zadnje_dodane_kartice()

    #3. dobi kljucne
    kljucne_skupaj = request.forms.get('kljucne')
    kljucne = locevanje_kljucnih_besed(kljucne_skupaj)

    #4. dobi orodja
    #so primeri, ko kartica uči več kot 1 orodje, zato je orodje tipa seznam:
    orodje = request.forms.getlist('orodje')
    print(orodje)

    #uporabnik vnese orodje, ki ga še ni v bazi:
    novo_orodje = request.forms.get('novo')
    if novo_orodje != '':
        #če tega orodja res ni v bazi: ga dodaj v bazo

        #spomnimo se:
        #~~ modeli.nastej_orodja()[0][0], modeli.nastej_orodja()[5][1])
        #~~ 1. stolpec 1. vrstice       , 2. stolpec 6. vrstice

        #seznam vrstic iz tabele programsko_orodje_ali_jezik[ime_orodja, id]
        vrstica = modeli.nastej_orodja()

        for orodje in vrstica:
            if vrstica[0] == novo_orodje:  #orodje ze obstaja
                id_novega_orodja = vrstica[1]  #PREVERITI, ALI ZE V SEZNAMU orodje?
                modeli.kartica_uci_programsko_orodje_jezik(id_kartice,
                                                           id_novega_orodja)

                #treba je samo vnesti povezavo kartica<--->to_orodje v tabelo
                #kartica_uci_programsko_orodje_jezik
                
            else:  #ime novega orodja se razlikuje od vseh obstojecih
                modeli.dodaj_orodje(novo_orodje)
                id_novega_orodja = modeli.id_zadnjega_dodanega_orodja()
                
                #rabimo, da tudi novo orodje pripisemo ravno dodani kartici:
                orodje.append(novo_orodje)    
    # v glavnem, zdaj imamo seznam orodij od te kartice
    # vnesemo v tabelo kartica_uci_programsko_orodje_jezik
    modeli.kartica_uci_programsko_orodje_jezik(id_kartice, orodje)
        
    return 'Dodajanje nove kartice je bilo uspešno.'

##############################################################################
# 
##############################################################################

run(debug=True)
