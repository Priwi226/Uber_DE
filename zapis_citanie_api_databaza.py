#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:09:51 2023
@author: priwi
"""

import sqlite3
import requests
import Nadstavenia
import importlib
import os 

user_name = os.getlogin()

def geocode(adresa):
    importlib.reload(Nadstavenia)
    # Funkcia na získanie geografických údajov z Google Maps API
    api_key = Nadstavenia.Googleapi
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={adresa}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK" and len(data["results"]) > 0:
        result = data["results"][0]
        formatted_address = result["formatted_address"]
        location = result["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        link = f"https://maps.google.com/?q={latitude},{longitude}&elevation=N/A"
        return formatted_address, link
    return None, None

def najdi_adresu(adresa):
    conn = sqlite3.connect(f"/home/{user_name}/Databaza/gmp.db")
    cursor = conn.cursor()
    
    importlib.reload(Nadstavenia)
    
    Google_on_api = Nadstavenia.Google_on_api

    total_address = None  # Přiřazení výchozí hodnoty None

    if Google_on_api == 1:
        # Hľadanie adresy v tabuľke t_aliases podľa aliasu
        cursor.execute("SELECT id_address FROM t_aliases WHERE alias = ?", (adresa,))
        id_address = cursor.fetchone()

        if id_address is None:
            # Adresa nebola nájdená v tabuľke t_aliases, získame ju z Google Maps API
            total_address, link = geocode(adresa)

            if total_address is not None:
                source = "Google Maps API"
                
                # Uloženie adresy do tabuľky t_addresses
                cursor.execute("INSERT INTO t_addresses (total_address, link) VALUES (?, ?)", (total_address, link))
                id_address = cursor.lastrowid

                # Uloženie aliasu do tabuľky t_aliases
                cursor.execute("INSERT INTO t_aliases (id_address, alias) VALUES (?, ?)", (id_address, adresa))
            else:
                total_address = adresa
                link = None
                source = "Pôvodný vstup"

        else:
            # Adresa bola nájdená v tabuľke t_aliases, získame ju z tabuľky t_addresses
            cursor.execute("SELECT id_address, total_address, link FROM t_addresses WHERE id_address = ?", (id_address[0],))
            id_address, total_address, link = cursor.fetchone()

            source = "Databáza"

    else:
        id_address = None
        total_address = adresa
        link = None
        source = "Pôvodný vstup"

    conn.commit()
    conn.close()

    return id_address, total_address, link, source


