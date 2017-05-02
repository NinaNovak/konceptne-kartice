SELECT konceptna_kartica.id AS ID,
       naslov_kartice AS naslov,
       replace(group_concat(distinct kljucna_beseda.beseda), ",", ", ") AS kljucne,
       replace(group_concat(distinct programsko_orodje_ali_jezik.ime_orodja), ",", ", ") AS orodja
  FROM konceptna_kartica
       JOIN
       povezovalna_tabela_konceptna_kartica_x_kljucna_beseda ON konceptna_kartica.id = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_konceptne_kartice
       JOIN
       kljucna_beseda ON kljucna_beseda.id = povezovalna_tabela_konceptna_kartica_x_kljucna_beseda.id_kljucne_besede
       JOIN
       povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik ON konceptna_kartica.id = povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_konceptne_kartice
       JOIN
       programsko_orodje_ali_jezik ON povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik.id_programskega_orodja_ali_jezika = programsko_orodje_ali_jezik.id
group by konceptna_kartica.id;


alter table povezovalna_tabela_konceptna_kartica_x_kljucna_beseda add primary key (id_konceptne_kartice,id_kljucne_besede);
alter table povezovalna_tabela_konceptna_kartica_x_programsko_orodje_ali_jezik add primary key (id_konceptne_kartice,id_programskega_orodja_ali_jezika);

ALTER TABLE povezovalna_tabela_konceptna_kartica_x_kljucna_beseda
ADD CONSTRAINT sestavljeni_kljuc PRIMARY KEY (id_konceptne_kartice,id_kljucne_besede);

SQLite supports a limited subset of ALTER TABLE. The ALTER TABLE command in SQLite allows the user to rename a table or to add a new column to an existing table. It is not possible to rename a colum, remove a column, or add or remove constraints from a table.
----------------------------------------------------
PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM test_tabela;

DROP TABLE test_tabela;

CREATE TABLE test_tabela (
    col1  PRIMARY KEY,
    col2
);

INSERT INTO test_tabela (
                            col1,
                            col2
                        )
                        SELECT col1,
                               col2
                          FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;
-------------------------------------------------