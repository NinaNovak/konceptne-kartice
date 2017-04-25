import sqlite3

con = sqlite3.connect('konceptnekartice.db')
con.row_factory = sqlite3.Row

##########################################################################
# kompletna tabela konceptnih kartic
##########################################################################

def vrni_tabelo_konceptnih():
    '''Vrne tabelo...'''
    sql = '''SELECT naslov_kartice AS naslov,
                    kljucna_beseda.beseda AS kljucne,
                    programsko_orodje_ali_jezik.ime_orodja AS orodja
             FROM konceptna_kartica JOIN
                  kartica_vsebuje_kljucno_besedo ON
                  konceptna_kartica.id =
                  kartica_vsebuje_kljucno_besedo.id_kartice JOIN
                  kljucna_beseda ON
                  kljucna_beseda.id =
                  kartica_vsebuje_kljucno_besedo.id_besede JOIN
                  kartica_uci_programsko_orodje_jezik ON
                  konceptna_kartica.id =
                  kartica_uci_programsko_orodje_jezik.id_kartice JOIN
                  programsko_orodje_ali_jezik ON
                  kartica_uci_programsko_orodje_jezik.id_orodja =
                  programsko_orodje_ali_jezik.id
          '''
    return list(con.execute(sql))

def vrni_vse_kljucne():
    '''Vrne tabelo...'''
    sql = '''SELECT *
             FROM kljucna_beseda
          '''
    return list(con.execute(sql))

##########################################################################
# konceptne kartice
##########################################################################

def vrni_kartico(id_kartice):
    sql = '''SELECT '''

def id_zadnje_dodane_kartice():
    #Za tabele v zvezi s ključnimi besedami in programskimi orodji
    #potrebujemo id ravnokar vnešene kartice. Ker je bil ta id
    #z autoincrement ustvarjen ravnokar, je zadnji => najvecji. Zato ga
    #klicemo z MAX(id).
    sql0 = '''
        SELECT MAX(id) as trenutna_kartica FROM konceptna_kartica
        '''
    id_kartice = con.execute(sql0).fetchone()
    return id_kartice

def dodaj_kartico(naslov_kartice, ime_datoteke):
    '''Doda kartico v bazo.'''
    #naslov_kartice, ime_datoteke - niza
    #vnašanje v tabelo konceptne_kartice
    sql = '''
        INSERT INTO konceptna_kartica (naslov_kartice, ime_datoteke)
        VALUES (?, ?)
        '''
    con.execute(sql, [naslov_kartice, ime_datoteke])
    con.commit()

def vrni_kartico(): pass

##########################################################################
# ?
##########################################################################

def shrani_pdf_v_blob(pdf_datoteka):
    '''Shrani pdf v bazo kot BLOB.'''
    sql = '''
        INSERT INTO konceptna_kartica

        '''

##########################################################################
# kljucne besede
##########################################################################

def id_kljucne_besede(beseda):
    sql = '''SELECT id FROM kljucna_beseda WHERE beseda = ?'''
    id_besede = con.execute(sql, [beseda]).fetchone()
    id_besede = id_besede[0]
    return id_besede

def vrni_vse_kljucne_besede():
    '''Vrne seznam vseh kljucnih besed v bazi.'''
    
    sql = '''SELECT beseda FROM kljucna_beseda'''
    vse_vrstice = list(con.execute(sql))
    vse_besede = []
    for b in vse_vrstice:
        vse_besede.append(b[0])
    return vse_besede

def dodaj_kljucno_besedo(beseda):
    '''V tabelo kljucne_besede vnese novo kljucno besedo.'''
    sql = '''
        INSERT INTO kljucna_beseda (beseda)
        VALUES (?)
        '''
    con.execute(sql, [beseda])
    con.commit()

def id_zadnje_kljucne_besede():
    #id zadnje kartice je bil z autoincrement ustvarjen ravnokar;
    #zato je zadnji => najvecji. Zato ga klicemo z MAX(id).
    sql = '''
        SELECT MAX(id) as id_zadnje FROM kljucna_beseda
        '''
    id_kljucne = con.execute(sql).fetchone()
    return id_kljucne

def kartica_ima_kljucne(id_kartice, seznam_besed):
    ''''''
    vse = vrni_vse_kljucne_besede()  #vse kljucne v bazi
    sez_idjev = []  #seznam id-jev kljucnih besed
    sql = '''INSERT INTO kartica_vsebuje_kljucno_besedo (id_kartice, id_besede)
            VALUES (?, ?)'''
    for beseda in seznam_besed:        
        #ce besede ni v bazi, jo dodamo
        if beseda not in vse:
            dodaj_kljucno_besedo(beseda)
            id_zadnje = id_zadnje_kljucne_besede()
            id_zadnje = id_zadnje[0]
            sez_idjev.append(id_zadnje)
        else:
            id_besede = id_kljucne_besede(beseda)
            sez_idjev.append(id_besede)
    #izpolnimo tabelo kartica_vsebuje_kljucno_besedo
    for id_kljucne in sez_idjev:
        con.execute(sql, [id_kartice, id_kljucne])
    con.commit()

def vrni_sez_kljucnih_za_eno_kartico(id_kartice):
    '''Za vse.tpl. Vrne seznam ključnih besed za id_kartice.'''
    sql = '''SELECT id_besede
        FROM kartica_vsebuje_kljucno_besedo
        WHERE id_kartice = ?'''
    seznam = list(con.execute(sql, [id_kartice]))
    sez = []  #seznam id-jev besed ~ nizov, ne id-jev besed ~ objektov
    for b in seznam:
        sez.append(b[0])
    #########
    sql_beseda = '''SELECT beseda
                FROM kljucna_beseda
                WHERE id = ?'''
    seznam_besed = []
    for id_besede in sez:
        beseda = con.execute(sql_beseda, [id_besede]).fetchone()[0]
        seznam_besed.append(beseda)
    return seznam_besed

##########################################################################
# programsko orodje/jezik
##########################################################################

def nastej_orodja():
    '''Vrne vsa orodja (id, ime_orodja) iz baze podatkov.'''
    sql = '''
        SELECT *
        FROM programsko_orodje_ali_jezik
        ORDER BY ime_orodja ASC
        '''
    seznam_vrstic = list(con.execute(sql))
    seznam_dvojic = []
    for v in seznam_vrstic:
        seznam_dvojic.append((v[0], v[1]))    
    return seznam_dvojic

def vrni_ime_orodja(id_orodja):
    '''Vrne ime orodja, ki pripada danemu id-ju.'''
    sql = '''SELECT ime_orodja
        FROM programsko_orodje_ali_jezik
        WHERE id = ?'''
    ime = con.execute(sql, [id_orodja]).fetchone()
    ime = ime[0]
    return ime

def dodaj_orodje(novo):
    '''Doda orodje novo v tabelo orodij.'''
    sql = '''
        INSERT INTO programsko_orodje_ali_jezik (ime_orodja)
        VALUES (?)
        '''
    con.execute(sql, [novo])
    con.commit()

def id_zadnjega_dodanega_orodja():
    #Ker je bil ta id z autoincrement ustvarjen ravnokar,
    #je zadnji => najvecji. Zato ga klicemo z MAX(id).
    sql = '''
        SELECT MAX(id) as id_zadnjega FROM programsko_orodje_ali_jezik
        '''
    id_zadnjega = con.execute(sql).fetchone()
    return id_zadnjega

def kartica_uci_programsko_orodje_jezik(id_kartice, sez_id_orodij):
    '''Izpolni povezovalno tabelo kartica_uci_programsko_orodje_jezik.'''
    for id_orodja in sez_id_orodij:
        sql = '''
            INSERT INTO kartica_uci_programsko_orodje_jezik
                        (id_kartice, id_orodja)
            VALUES (?, ?)
            '''
        con.execute(sql, [id_kartice, id_orodja])
    con.commit()
