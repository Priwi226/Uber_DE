#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 4 12:56:39 2023
@author: zuzana
"""

import sqlite3
import requests
import Nadstavenia
import os 

user_name = os.getlogin()



def spracovat_adresy(adresa1, adresa2, Google_on_api, Googleapi):
    # Pripojenie k SQLite databáze
    connection = sqlite3.connect(f"/home/{user_name}/Databaza/gmp.db")
    
    # Vytvorenie kurzora pre vykonávanie SQL príkazov
    cursor = connection.cursor()
    
    # Hľadanie adresa1 v tabuľke t_aliases
    cursor.execute('SELECT id_address FROM t_aliases WHERE alias = ?', (adresa1,))
    result = cursor.fetchone()
    
    if result is not None:
        # Adresa1 bola nájdená v tabuľke t_aliases
        id_address1 = result[0]
    else:
        # Adresa1 nebola nájdená v tabuľke t_aliases, prehľadávame tabuľku t_addresses
        cursor.execute('SELECT * FROM t_addresses WHERE total_address = ?', (adresa1,))
        result = cursor.fetchone()
        
        if result is not None:
            # Adresa1 bola nájdená v tabuľke t_addresses
            id_address1 = result[0]
        else:
            # Adresa1 nebola nájdená v tabuľke t_addresses
            id_address1 = None
    
    # Hľadanie adresa2 v tabuľke t_aliases
    cursor.execute('SELECT id_address FROM t_aliases WHERE alias = ?', (adresa2,))
    result = cursor.fetchone()
    
    if result is not None:
        # Adresa2 bola nájdená v tabuľke t_aliases
        id_address2 = result[0]
    else:
        # Adresa2 nebola nájdená v tabuľke t_aliases, prehľadávame tabuľku t_addresses
        cursor.execute('SELECT * FROM t_addresses WHERE total_address = ?', (adresa2,))
        result = cursor.fetchone()
        
        if result is not None:
            # Adresa2 bola nájdená v tabuľke t_addresses
            id_address2 = result[0]
        else:
            # Adresa2 nebola nájdená v tabuľke t_addresses
            id_address2 = None
    
    # Spracovanie výsledkov
    if id_address1 is not None and id_address2 is not None:
        # Hľadanie vzdialenosti v tabuľke t_vzdialenosti
        cursor.execute('SELECT vzdialenost, cas, cesta_link FROM t_vzdialenosti WHERE id_address_vyzdvihnutia = ? AND id_address_vylozenia = ?', (id_address1, id_address2))
        result = cursor.fetchone()
        
        if result is not None:
            vzdialenost = result[0]
            cas = result[1]
            cesta_link = result[2]
        else:
            vzdialenost = None
            cas = None
            cesta_link = None
    else:
        vzdialenost = None
        cas = None
        cesta_link = None
    
    # Uzavretie pripojenia a kurzora
    cursor.close()
    connection.close()
    
    # Vytvorenie vlastnej premennej source s textom "databaza"
    source = "Databaza"
    
    # Ak výsledky neboli nájdené v databáze a Google_on_api je zapnuté, vyhľadaj na Google Maps
    if vzdialenost is None and cas is None and Google_on_api == 1:
        key = Googleapi  # Použitie definovanej premennej Googleapi
        vzdialenost, cas = vyhladaj_google_maps(adresa1, adresa2, key)
        cesta_link = None
        source = "Google API"
        
        # Ak sú k dispozícii výsledky z Google Maps, uložte ich do databázy
        if vzdialenost is not None and cas is not None:
            zapis_dat_do_databazy(adresa1, adresa2, id_address1, id_address2, vzdialenost, cas, None)
    
    # Vrátenie výsledkov
    return vzdialenost, cas, cesta_link, source


def vyhladaj_google_maps(adresa1, adresa2, key):
    if adresa1 is None or adresa2 is None:
        return None, None

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={adresa1}&destination={adresa2}&key={key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        distance = data['routes'][0]['legs'][0]['distance']['text']
        duration = data['routes'][0]['legs'][0]['duration']['text']
    else:
        distance = None
        duration = None

    return distance, duration


def zapis_dat_do_databazy(adresa1, adresa2, id_address1, id_address2, vzdialenost, cas, cesta_link):
    # Pripojenie k SQLite databáze
    connection = sqlite3.connect('data/gmp.db')

    # Vytvorenie kurzora pre vykonávanie SQL príkazov
    cursor = connection.cursor()

    # Najdenie ID zaznamu v tabuľke t_aliases pre adresa1
    cursor.execute('SELECT id_address FROM t_aliases WHERE alias = ?', (adresa1,))
    result = cursor.fetchone()

    if result is not None:
        id_address_vyzdvihnutia = result[0]
    else:
        # Adresa1 nebola nájdená v tabuľke t_aliases, prehľadávame tabuľku t_addresses
        cursor.execute('SELECT id_address FROM t_addresses WHERE total_address = ?', (adresa1,))
        result = cursor.fetchone()

        if result is not None:
            id_address_vyzdvihnutia = result[0]
        else:
            id_address_vyzdvihnutia = None

    # Najdenie ID zaznamu v tabuľke t_aliases pre adresa2
    cursor.execute('SELECT id_address FROM t_aliases WHERE alias = ?', (adresa2,))
    result = cursor.fetchone()

    if result is not None:
        id_address_vylozenia = result[0]
    else:
        # Adresa2 nebola nájdená v tabuľke t_aliases, prehľadávame tabuľku t_addresses
        cursor.execute('SELECT id_address FROM t_addresses WHERE total_address = ?', (adresa2,))
        result = cursor.fetchone()

        if result is not None:
            id_address_vylozenia = result[0]
        else:
            id_address_vylozenia = None

    # Vytvorenie cesty link
    if adresa1 is not None and adresa2 is not None:
        cesta_link = f"https://www.google.com/maps/dir/?api=1&origin={adresa1}&destination={adresa2}&travelmode=car"
    else:
        cesta_link = None

    # Vloženie údajov do tabuľky t_vzdialenosti
    cursor.execute('INSERT INTO t_vzdialenosti (id_address_vyzdvihnutia, id_address_vylozenia, vzdialenost, cas, cesta_link) VALUES (?, ?, ?, ?, ?)', (id_address_vyzdvihnutia, id_address_vylozenia, vzdialenost, cas, cesta_link))

    # Potvrdenie transakcie a ukončenie
    connection.commit()
    cursor.close()
    connection.close()



# # Volanie funkcie s vstupnými adresami
# adresa1 = "Walter-Paetzmann-Straße 1 Unterhaching 82008"
# adresa2 = "Hans-Denzinger-Straße 23 München 80807"
# vzdialenost, cas, cesta_link, source = spracovat_adresy(adresa1, adresa2,  Nadstavenia.Google_on_api, Nadstavenia.Googleapi)

# #Výpis výsledkov
# print("Vzdialenosť: ", vzdialenost)
# print("Čas: ", cas)
# print("Cesta link: ", cesta_link)
# print("Zdroj údajov: ", source)
