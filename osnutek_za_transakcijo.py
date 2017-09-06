def transakcija():
    '''Dodajanje 1 kartice v bazo.'''

    #kličemo že napisane funkcije v modeli.py

    #izpolni tabelo KK
    dodaj_kartico(ime_kartice, nalozena_datoteka.filename)

    # ? id_zadnje_dodane_kartice

    #izpolni povezovalno tabelo __KK in ključne__
    kartica_ima_kljucne(id_kartice, kljucne)

    #izpolni povezovalno tabelo __KK in PJ__
    kartica_uci_programsko_orodje_jezik(id_kartice, sez_ID_orodij)
    #še enkrat?
    kartica_uci_programsko_orodje_jezik(id_kartice, [id_orodja])

    #izpis o uspeli transakciji
    vrni_ime_orodja(id_orodja)
    
