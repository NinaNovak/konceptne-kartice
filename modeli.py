import sqlite3

conn = sqlite3.connect('konceptnekartice.db')
conn.row_factory = sqlite3.Row

##############################################################################
# kompletna tabela konceptnih kartic
##############################################################################
def vrni_tabelo_konceptnih():
    '''Vrne tabelo VSEH kartic:

        njihove ID-je, naslove, kljucne besede in
        programska orodja oziroma jezike, ki jih kartica uci,
        ter ime datoteke.

        '''
    
    sql = '''SELECT konceptna_kartica.id AS id_konceptne,
       naslov_kartice AS naslov,
       replace(group_concat(distinct kljucna_beseda.beseda), ",", ", ") AS kljucne,
       replace(group_concat(distinct programsko_orodje_ali_jezik.ime_orodja), ",", ", ") AS orodja,
       ime_PDF_datoteke AS dat,
       ime_datoteke AS dat_orig,
       kratek_opis AS opis
       FROM konceptna_kartica
       JOIN
       povezovalna_tabela_konceptna_kartica_x_kljucna_beseda
       ON
       konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_konceptne_kartice
       JOIN
       kljucna_beseda
       ON
       kljucna_beseda.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_kljucne_besede
       JOIN
       povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik ON konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_konceptne_kartice
       JOIN
       programsko_orodje_ali_jezik
       ON
       povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_programskega_orodja_ali_jezika
       = programsko_orodje_ali_jezik.id
       GROUP BY konceptna_kartica.id
          '''
    return list(conn.execute(sql))
##############################################################################
def vrni_konceptne_rezultat_iskanja(sez_iskalnih_besed):
    """Vrne rezultat za polje IŠČI."""

    st_iskalnih_besed = len(sez_iskalnih_besed)

    if st_iskalnih_besed == 0:  #1. robni primer
        #za prazen iskalni niz vrnemo vse konceptne kartice
        return vrni_tabelo_konceptnih()

    #string se mora obvezno koncati z \n
    za_vsako_naslednjo_kljucno = ' ' + '''OR    naslov_kartice_in_vse_kljucne_in_vsi_jeziki LIKE '% ' || ? || ' %'  --naslednja iskalna beseda''' + '\n '

    if st_iskalnih_besed == 1:  #2. robni primer
        za_vsako_naslednjo_kljucno = ''

    #3. robni primer: iskalni niz je npr. "py" (samo del iskane besede)

    sql = '''

SELECT id_konceptne, naslov, kljucne, orodja, dat FROM   
(
    SELECT konceptna_kartica.id AS id_konceptne,
       naslov_kartice AS naslov,
       replace(group_concat(distinct kljucna_beseda.beseda), ",", ", ") AS kljucne,
       replace(group_concat(distinct programsko_orodje_ali_jezik.ime_orodja), ",", ", ") AS orodja,
       ime_PDF_datoteke AS dat,
       ime_datoteke AS dat_orig,
            ' ' || naslov_kartice
           || ' ' || replace(group_concat(distinct beseda), ",", " ")
           || ' ' || replace(group_concat(distinct ime_orodja), ",", " ")
           || ' '
           AS naslov_kartice_in_vse_kljucne_in_vsi_jeziki,
       kratek_opis AS opis
    FROM konceptna_kartica
       JOIN povezovalna_tabela_konceptna_kartica_x_kljucna_beseda
       ON konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_konceptne_kartice
       JOIN kljucna_beseda
       ON kljucna_beseda.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_kljucne_besede
       JOIN povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik
       ON konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_konceptne_kartice
       JOIN programsko_orodje_ali_jezik
       ON povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_programskega_orodja_ali_jezika
       = programsko_orodje_ali_jezik.id
    GROUP BY konceptna_kartica.id
)
WHERE naslov_kartice_in_vse_kljucne_in_vsi_jeziki LIKE '% ' || ? || ' %'  --prva iskalna beseda

    ''' + za_vsako_naslednjo_kljucno * (len(sez_iskalnih_besed) - 1)
    return list(conn.execute(sql, sez_iskalnih_besed))
##############################################################################
def vrni_konceptne_po_jezikih(jezik):
    '''Vrne tabelo kartic za izbrani jezik'''
    
    sql = '''SELECT konceptna_kartica.id AS ID,
       naslov_kartice AS naslov,
       replace(group_concat(distinct kljucna_beseda.beseda), ",", ", ") AS kljucne,
       replace(group_concat(distinct programsko_orodje_ali_jezik.ime_orodja), ",", ", ") AS orodja,
       ime_PDF_datoteke AS dat,
       ime_datoteke AS dat_orig,
       kratek_opis AS opis
FROM konceptna_kartica
       JOIN povezovalna_tabela_konceptna_kartica_x_kljucna_beseda
       ON konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_konceptne_kartice
       JOIN kljucna_beseda
       ON kljucna_beseda.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_kljucne_besede
       JOIN povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik
       ON konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_konceptne_kartice
       JOIN programsko_orodje_ali_jezik
       ON povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_programskega_orodja_ali_jezika
       = programsko_orodje_ali_jezik.id
GROUP BY konceptna_kartica.id
HAVING ' ' || replace(group_concat(distinct programsko_orodje_ali_jezik.id), ",", " ") || ' ' LIKE '% ' || ? || ' %'
              
       '''
    
    return list(conn.execute(sql, [jezik]))
##############################################################################
def vrni_tabelo_konceptnih_izjema():
    sql = '''SELECT konceptna_kartica.id AS id_konceptne,
       naslov_kartice AS naslov,
       replace(group_concat(distinct kljucna_beseda.beseda), ",", ", ") AS kljucne,
       replace(group_concat(distinct programsko_orodje_ali_jezik.ime_orodja), ",", ", ") AS orodja
       FROM konceptna_kartica
       JOIN
       povezovalna_tabela_konceptna_kartica_x_kljucna_beseda
       ON
       konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_konceptne_kartice
       JOIN
       kljucna_beseda
       ON
       kljucna_beseda.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_kljucne_besede
       JOIN
       povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik ON konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_konceptne_kartice
       JOIN
       programsko_orodje_ali_jezik
       ON
       povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_programskega_orodja_ali_jezika
       = programsko_orodje_ali_jezik.id
       GROUP BY konceptna_kartica.id
       HAVING id_konceptne = '-1'
          '''
    return list(conn.execute(sql))
##############################################################################
def vrni_eno_kartico(idkartice):
    '''Vrne tabelo s podatki za kartico z izbranim ID-jem:

        njen naslov, kljucne besede in
        programska orodja oziroma jezike, ki jih kartica uci
        ter ime datoteke.

        '''

    sql = '''SELECT naslov_kartice AS naslov,
       replace(group_concat(distinct kljucna_beseda.beseda), ",", ", ") AS kljucne,
       replace(group_concat(distinct programsko_orodje_ali_jezik.ime_orodja), ",", ", ") AS orodja,
       ime_PDF_datoteke AS dat,
       ime_datoteke AS dat_orig       
       FROM konceptna_kartica
       JOIN
       povezovalna_tabela_konceptna_kartica_x_kljucna_beseda
       ON
       konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_konceptne_kartice
       JOIN
       kljucna_beseda
       ON
       kljucna_beseda.id
       = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_kljucne_besede
       JOIN
       povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik ON konceptna_kartica.id
       = povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_konceptne_kartice
       JOIN
       programsko_orodje_ali_jezik
       ON
       povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_programskega_orodja_ali_jezika
       = programsko_orodje_ali_jezik.id

       WHERE konceptna_kartica.id = ?
       
       '''
    kartica = conn.execute(sql, [idkartice]).fetchone()
    return kartica
##############################################################################
# konceptne kartice - razno
##############################################################################
def id_zadnje_dodane_kartice():
    #Za tabele v zvezi s ključnimi besedami in programskimi orodji
    #potrebujemo id ravnokar vnešene kartice. Ker je bil ta id
    #z autoincrement ustvarjen ravnokar, je zadnji => najvecji. Zato ga
    #klicemo z MAX(id).
    sql0 = '''
        SELECT MAX(id) as trenutna_kartica FROM konceptna_kartica
        '''
    id_kartice = conn.execute(sql0).fetchone()
    return id_kartice

def dodaj_kartico(naslov_kartice, ime_datoteke, ime_PDF_datoteke):
    '''Doda kartico v bazo.'''
    #naslov_kartice, ime_datoteke - niza
    #vnašanje v tabelo konceptne_kartice
    sql = '''
        INSERT INTO konceptna_kartica (naslov_kartice,
                                         ime_datoteke,
                                         ime_PDF_datoteke)
        VALUES (?, ?, ?)
        '''
    conn.execute(sql, [naslov_kartice, ime_datoteke, ime_PDF_datoteke])
    conn.commit()
##############################################################################
# kljucne besede
##############################################################################
def vrni_vse_kljucne():
    '''Vrne tabelo...'''
    sql = '''SELECT *
             FROM kljucna_beseda
          '''
    return list(conn.execute(sql))

def id_kljucne_besede(beseda):
    sql = '''SELECT id FROM kljucna_beseda WHERE beseda = ?'''
    id_besede = conn.execute(sql, [beseda]).fetchone()
    id_besede = id_besede[0]
    return id_besede

def vrni_vse_kljucne_besede():
    '''Vrne seznam vseh kljucnih besed v bazi.'''
    
    sql = '''SELECT beseda FROM kljucna_beseda'''
    vse_vrstice = list(conn.execute(sql))
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
    conn.execute(sql, [beseda])
    conn.commit()

def id_zadnje_kljucne_besede():
    #id zadnje kartice je bil z autoincrement ustvarjen ravnokar;
    #zato je zadnji => najvecji. Zato ga klicemo z MAX(id).
    sql = '''
        SELECT MAX(id) as id_zadnje FROM kljucna_beseda
        '''
    id_kljucne = conn.execute(sql).fetchone()
    return id_kljucne

def kartica_ima_kljucne(id_kartice, seznam_besed):
    '''Ob dodajanju nove kartice vnese v povezovalno tabelo vse ključne besede,
        vse ključne besede, ki pripadajo tej kartici.'''
    vse = vrni_vse_kljucne_besede()  #vse kljucne v bazi
    sez_idjev = []  #seznam id-jev kljucnih besed
    sql = '''INSERT INTO povezovalna_tabela_konceptna_kartica_x_kljucna_beseda (id_konceptne_kartice, id_kljucne_besede)
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
    #izpolnimo tabelo povezovalna_tabela_konceptna_kartica_x_kljucna_beseda
    for id_kljucne in sez_idjev:
        conn.execute(sql, [id_kartice, id_kljucne])
    conn.commit()

def vrni_sez_kljucnih_za_eno_kartico(id_kartice):
    '''Za vse.tpl. Vrne seznam ključnih besed za id_kartice.'''
    sql = '''SELECT id_kljucne_besede
        FROM povezovalna_tabela_konceptna_kartica_x_kljucna_beseda
        WHERE id_konceptne_kartice = ?'''
    seznam = list(conn.execute(sql, [id_kartice]))
    sez = []  #seznam id-jev besed ~ nizov, ne id-jev besed ~ objektov
    for b in seznam:
        sez.append(b[0])
    #########
    sql_beseda = '''SELECT beseda
                FROM kljucna_beseda
                WHERE id = ?'''
    seznam_besed = []
    for id_besede in sez:
        beseda = conn.execute(sql_beseda, [id_besede]).fetchone()[0]
        seznam_besed.append(beseda)
    return seznam_besed
##############################################################################
# programsko orodje/jezik
##############################################################################
def orodja_od_1_kartice(id_kartice):
    '''Vrne seznam orodij (id, ime) za 1 kartico.'''
    sql = '''
        SELECT povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_programskega_orodja_ali_jezika AS id_o,
        programsko_orodje_ali_jezik.ime_orodja
        FROM povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik
        JOIN programsko_orodje_ali_jezik
        ON id_o =
        programsko_orodje_ali_jezik.id
        WHERE id_konceptne_kartice = ?

        '''
    orodja = list(conn.execute(sql, [id_kartice]))
    return orodja
def nastej_orodja():
    '''Vrne vsa orodja (id, ime_orodja) iz baze podatkov.'''
    sql = '''
        SELECT *
        FROM programsko_orodje_ali_jezik
        ORDER BY ime_orodja ASC
        '''
    seznam_vrstic = list(conn.execute(sql))
    seznam_dvojic = []
    for v in seznam_vrstic:
        seznam_dvojic.append((v[0], v[1]))    
    return seznam_dvojic

def vrni_ime_orodja(id_orodja):
    '''Vrne ime orodja, ki pripada danemu id-ju.'''
    sql = '''SELECT ime_orodja
        FROM programsko_orodje_ali_jezik
        WHERE id = ?'''
    ime = conn.execute(sql, [id_orodja]).fetchone()
    ime = ime[0]
    return ime

def dodaj_orodje(novo):
    '''Doda orodje novo v tabelo orodij.'''
    sql = '''
        INSERT INTO programsko_orodje_ali_jezik (ime_orodja)
        VALUES (?)
        '''
    conn.execute(sql, [novo])
    conn.commit()

def id_zadnjega_dodanega_orodja():
    #Ker je bil ta id z autoincrement ustvarjen ravnokar,
    #je zadnji => najvecji. Zato ga klicemo z MAX(id).
    sql = '''
        SELECT MAX(id) as id_zadnjega FROM programsko_orodje_ali_jezik
        '''
    id_zadnjega = conn.execute(sql).fetchone()
    return id_zadnjega[0]

def kartica_uci_programsko_orodje_jezik(id_kartice, sez_id_orodij):
    '''Izpolni povezovalno tabelo povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.'''
    for id_orodja in sez_id_orodij:
        sql = '''
            INSERT INTO povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik
                        (id_konceptne_kartice, id_programskega_orodja_ali_jezika)
            VALUES (?, ?)
            '''
        conn.execute(sql, [id_kartice, id_orodja])
    conn.commit()
##############################################################################
# ID-JI VSEH KARTIC
##############################################################################
def vrni_imena_datotek_vseh_kartic():
    '''Vrne seznam imen vseh konceptnih kartic, ki so v bazi.'''
    
    sql = '''SELECT ime_PDF_datoteke FROM konceptna_kartica'''
    vse_vrstice = list(conn.execute(sql))
    vsa_imena = []
    for kartica in vse_vrstice:
        vsa_imena.append(vse_vrstice[0])
    return vsa_imena
##############################################################################
# THE END
##############################################################################
