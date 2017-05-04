    sql = '''

    SELECT konceptna_kartica.id AS ID,
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
       
WHERE konceptna_kartica.id IN
-------------------------------------------------------------------------
(SELECT id_konceptne FROM   
--------------------------------------------------------------------------
    (SELECT konceptna_kartica.id AS id_konceptne,

              ' '
           || naslov_kartice
           || ' '
           || replace(group_concat(distinct beseda), ",", " ")
           || ' '
           || replace(group_concat(distinct ime_orodja), ",", " ")
           || ' '

    AS naslov_kartice_in_vse_kljucne_in_vsi_jeziki

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
    
    )
--------------------------------------------konec SELECT-a
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
       JOIN programsko_orodje_ali_jezik
       ON povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_programskega_orodja_ali_jezika = programsko_orodje_ali_jezik.id
    
WHERE naslov_kartice_in_vse_kljucne_in_vsi_jeziki LIKE '% ' || ? || ' %'  --prva iskalna beseda
OR    naslov_kartice_in_vse_kljucne_in_vsi_jeziki LIKE '% ' || ? || ' %'  --druga iskalna beseda

)

-----------------------------------------------konec SELECTa

GROUP BY konceptna_kartica.id

    '''
