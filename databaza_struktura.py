databaza ma strukturu : tabulka1: sqlite_sequence = CREATE TABLE sqlite_sequence(name,seq) / name = "name" / seq = "seq"  ///tabulka2: t_addresses stlpce /id_address = INTEGER "id_address" INTEGER NOT NULL / total_address = TEXT "total_address" TEXT / country = TEXT
"country" TEXT / link = TEXT "link" TEXT / special = TEXT "special" TEXT /// tabulka3: t_aliases = CREATE TABLE "t_aliases" ( "id_alias"
INTEGER NOT NULL, "id_address" INTEGER
NOT NULL, "alias" TEXT NOT NULL, PRIMARY
KEY("id_alias" AUTOINCREMENT) ) / id_alias = INTEGER "id_alias" INTEGER NOT NULL / id_address = INTEGER "id_address" INTEGER NOT NULL / alias = TEXT "alias" TEXT NOT NULL///tabulka4: t_routes = CREATE TABLE "t_routes" ( "id_route"
INTEGER NOT NULL, "id_origin" INTEGER
NOT NULL, "id_destination" INTEGER NOT
NULL, "distance" INTEGER, "duration"
INTEGER, "duration_in_traffic" INTEGER,
"driving_date" TEXT, PRIMARY
KEY("id_route" AUTOINCREMENT) ) / id_route = INTEGER "id_route" INTEGER NOT NULL / id_origin = INTEGER "id_origin" INTEGER NOT NULL / id_destination = INTEGER "id_destination" INTEGER NOT NULL / distance = INTEGER "distance" INTEGER / duration = INTEGER "duration" INTEGER / duration_in_traﬃc = INTEGER "duration_in_traﬃc" INTEGER / driving_date =  TEXT"driving_date" TEXT /// Tabulka5: CREATE TABLE t_vzdialenosti (
id_vzdialenost INTEGER PRIMARY KEY
AUTOINCREMENT, id_address_vyzdvihnutia
INTEGER, id_address_vylozenia INTEGER,
vzdialenost TEXT, cas TEXT, cas_zapcha
TEXT, cesta_link TEXT, FOREIGN KEY
(id_address_vyzdvihnutia) REFERENCES
t_addresses (id_address), FOREIGN KEY
(id_address_vylozenia) REFERENCESt_addresses (id_address) ) / id_vzdialenost = INTEGER "id_vzdialenost" INTEGER / id_address_vyzdvihnutia = INTEGER "id_address_vyzdvihnutia" INTEGER / id_address_vylozenia = INTEGER "id_address_vylozenia" INTEGER / vzdialenost = TEXT
"vzdialenost" TEXT / cas = TEXT"cas" TEXT / cas_zapchaTEXT"cas_zapcha" TEXT / cesta_linkTEXT"cesta_link" TEXT

citanie databazy 
budeme mat vstupne data : 
adresa1(start) a adresa 2(ciel)AUTOINCREMENT
adresa1 najprv bude overena tabulka: t_aliases stlpec: alias ci tam adresa nachadza ak ano v tom pripade si ulozime z toho riadku id_address nasledne prejdem do do tabulky t_addresses kde podla id_address vyhladame kompletnu infomaciu o adrese (cely riadok) 
ak data nenajdeme v tabulke t_aliases tak automaticky  prehladame tabulku t_addresses stlpec total_address ak tam bude zhoda ulozime si kopletne data o adresse (celiriadok) 
Nasledne prejdeme do do tabulky t_vzdialenosti kde vyhladame adresa1(adresa vazdvyhnutia) a v stlpci id_address_vyzdvihnutia hladame ulozene id_address nasledne hladame vstlpci id_address_vylozenia adresa2(adresa vylozenia)podla id_address. Ak najdeme zhodu v obochudajoch takodcitame zvysok tabulky: vzdialenost cas cestalink a tieto veliciny ulozine v pythone pod osobytne premmene
plus python vyvytvory vlastnu velicinu source ktora bude obsahovat text databaza
pokial nenajdeme zhodu vsetkym velicinam vpythonpriradime hodnotu None 

zapis do databazy
najdeme obe adresy v databaze v tabulke t_aliases stlpec: alias a ziskame id_address alebo v tabulke t_addresses v stplci total_address nasledne otvorime tabulku t_vzdialenosti a dostlpca id_address_vyzdvihnutia = id adresy vyzdvyhnutia ; id_address_vylozenia = id adresy vylozenia; distance = ziskany udaj z google maps distanc ; cas = duration ; link = link aj jedna z tichto velicin chyba tak ju doplnime  



adresa1 najprv bude overena tabulka: t_aliases stlpec: alias ci tam adresa nachadza ak ano v tom pripade si ulozime z toho riadku id_address. Ak udaje nenajde tak prekontroluje t_addresses stlpec total_address a za tade pouzijeudaj id_address ten isti postup sa zopakuje aj pri adresa2