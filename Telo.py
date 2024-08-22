#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:09:51 2023
@author: priwi
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from colorama import init, Fore, Style
from datetime import datetime
import time
import importlib
import Nadstavenia
import zapis_citanie_api_databaza
import pocitanie_trasy 
import podmienka
from selenium import webdriver
import FTP
import threading
import porovnanie
import re
import Email
import schedule

def reload_modules():
    importlib.reload(Nadstavenia)
    importlib.reload(zapis_citanie_api_databaza)

init()

Rozdiel = None
Posledna_zakazka = None
old_tab = None
neu_tab = []

def Telo(driver, Posledna_zakazka, Adresa_vyzdvyhnutia, Adresa_vylozenia, old_tab):

    Rozdiel = None
    
    def run_data():
        while True:
            FTP.databaza_copy
            time.sleep(86000)

    thread = threading.Thread(target=run_data)
    thread.daemon = True  # Nastavenie vlákna ako démonského
    thread.start()
    
    while True:
        try: 
            ziadosti = driver.find_elements(By.XPATH, "//div[text()='There are no new requests' or text()='Nemáš nové žiadosti']")
            cas = datetime.now().time()
            Aktualny_cas = cas.strftime("%H:%M:%S")
            print('\n' + Style.BRIGHT + "Hľadám nové objednávky UBER " + Style.RESET_ALL + Aktualny_cas)
    
            if Posledna_zakazka is not None:
                print("Posledná objednávka:\n  " + Posledna_zakazka)
            if Rozdiel is not None and Rozdiel > 0:
                print("\033[1mZLA CENA: cena je nižšia o: \033[0m" + str(Rozdiel) + "€\033[0m")
            reload_modules()
    
            time.sleep(1)
            if len(ziadosti) == 0:
                # Nájdenie tabuľky pomocou className
                try:
                    table_body = driver.find_element(By.CLASS_NAME, "MuiTableBody-root")
                except StaleElementReferenceException:
                    driver.refresh()
                    # time.sleep(1)
                    continue
    
                # Nájdenie riadkov tabuľky
                rows = table_body.find_elements(By.TAG_NAME, 'tr')
    
                if len(rows) == 0:
                    continue
                
                # time.sleep(1)
    
                neu_tab = []
    
                # Prechádzanie jednotlivých riadkov a získavanie údajov
                try:
                    for riadok in rows:
                        # Získanie jednotlivých buniek
                        bunky = riadok.find_elements(By.TAG_NAME, 'td')
        
                        # Získanie údajov z buniek a pridanie do príslušnej premennej
                        cena = bunky[1].text
                        adresa_vyzdvyhnutia = bunky[2].text
                        adresa_vylozenia = bunky[3].text
                        meno_zakaznika = bunky[4].text
                        sofer = bunky[5].text
                        datum_prijatia = bunky[6].text
                        cas_prijatia = bunky[7].text
        
                        # Priradenie správneho buttonu
                        akcepte = riadok.find_element(By.TAG_NAME, 'button')
        
                        # Pridanie riadku do neu_tab
                        neu_tab.append((akcepte, cena, adresa_vyzdvyhnutia, adresa_vylozenia, meno_zakaznika, sofer, datum_prijatia, cas_prijatia))
    
                except StaleElementReferenceException:
                    driver.refresh()
                    time.sleep(1)
                    continue
    
                if old_tab == neu_tab:
                    # Ak sa tabuľky zhodujú, pokračuje sa v ďalšom kóde
                    time.sleep(1)
                    print("Tabuľky sa zhodujú. Nevykonávam žiadnu akciu.")
                else:
                    # Ak sa tabuľky nezhodujú, vykonávajú sa príslušné akcie
                    print("Zmena v tabuľke. Vykonávam príslušné akcie.")
                    Rozdiel = None
    
                    for riadok in neu_tab:
                        akcepte = riadok[0]
                        Cena_t = riadok[1]
                        Adresa_vyzdvyhnutia = riadok[2]
                        Adresa_vylozenia = riadok[3]
                        Meno_zakaznika = riadok[4]
                        Sofer = riadok[5]
                        Datum_prijatia = riadok[6]
                        Cas_prijatia = riadok[7]
    
                    old_tab = neu_tab
                    
                    cas = datetime.now().time()
                    Aktualny_cas = cas.strftime("%H:%M:%S")
                    print('\033[1m' + "     Nájdená nová objednávka     " + '\033[0m' + Aktualny_cas)
    
                        # overenie ci Cena ma normalne znaky. ak nie tak dostane hodotu None
                    # Nahraďte desatinnú čiarku bodkou a odstráňte ostatné nepovolené znaky okrem čísel
                    Cena_n = re.sub(r"[^0-9.,]", "", Cena_t)
                    Cena_n = Cena_n.replace(",", ".")
    
                    # Ak Cena nie je prázdna
                    if Cena_n:
                        # Skonvertujte reťazec na float
                        Cena = float(Cena_n)
                        print(Cena)
                    else:
                        Cena = "Preis"
    
                    # Kontrola dĺžky reťazca
                    if Cena is not None:
                        Cena_str = str(Cena)
                        len(Cena_str)
    
                    print(Cena)
                    print(type(Cena))
                    
                    print(Cena)
                    print(type(Cena))
                    print(Adresa_vyzdvyhnutia)
                    print(type(Adresa_vyzdvyhnutia))
                    print(Adresa_vylozenia)
                    print(type(Adresa_vylozenia))
                    print(meno_zakaznika)
                    print(type(meno_zakaznika))
                    print(Sofer)
                    print(type(Sofer))
                    print(Datum_prijatia)
                    print(type(Datum_prijatia))
                    print(Cas_prijatia)
                    print(type(Cas_prijatia))
    
                    Adresa_Vyzdvyhnutia = Adresa_vyzdvyhnutia
    
                        
                    # Nastavenie adries pre Google Maps
                        # Zmeny adries aliasov
                            # Adresa vyzdvyhnutia
                    if "Terminal" in Adresa_Vyzdvyhnutia:
                        Adresa_Vyzdvyhnutia = "Nordallee 25, 85356 München-Flughafen"
                    if "Messe Ost" in Adresa_Vyzdvyhnutia:
                        Adresa_Vyzdvyhnutia = "Am Messesee 2, 81829 München"
                    if "Oktoberfest" in Adresa_Vyzdvyhnutia:
                        Adresa_Vyzdvyhnutia = "St.-Pauls-Platz 11, 80336 München"
                    if "Theresienwiese" in Adresa_Vyzdvyhnutia:
                        Adresa_Vyzdvyhnutia = "St.-Pauls-Platz 11, 80336 München"

    
                            # Adresa Vylozenia 
                    if "Terminal" in Adresa_vylozenia:
                        Adresa_vylozenia = "Nordallee 25, 85356 München-Flughafen"
                    if "Messe Ost" in Adresa_vylozenia:
                        Adresa_Vyzdvyhnutia = "Am Messesee 2, 81829 München"
                    if "Oktoberfest" in Adresa_vylozenia:
                        Adresa_vylozenia = "St.-Pauls-Platz 11, 80336 München"
                    if "Theresienwiese" in Adresa_vylozenia:
                        Adresa_Vylozenia = "St.-Pauls-Platz 11, 80336 München"
    
                    id_address, total_address, link, source = zapis_citanie_api_databaza.najdi_adresu(Adresa_Vyzdvyhnutia)
                    id_Adresa_Vyzdvyhnutia = id_address
                    Adresa_Vyzdvyhnutia = total_address
                    start_link = link
                    if start_link == None:
                        start_link = ("http://maps.google.com/maps?q=" + Adresa_Vyzdvyhnutia)
                    source_vyzdvyhnutie = source
                    if source_vyzdvyhnutie == None:
                        source_vyzdvyhnutie = ("vstup")
                    id_address = None
                    total_address = None
                    link = None
                    source = None
                        ##################################################
                    id_address, total_address, link, source = zapis_citanie_api_databaza.najdi_adresu(Adresa_vylozenia)
                    id_Adresa_vylozenia = id_address
                    if id_Adresa_vylozenia == None:
                        id_Adresa_vylozenia = "x"
                    ciel_link = link
                    Adresa_Vylozenia = total_address
                    if Adresa_Vylozenia == None:
                        Adresa_Vylozenia = Adresa_vylozenia
                        ciel_link = link
                    if ciel_link == None:
                        ciel_link = ("http://maps.google.com/maps?q=" + Adresa_Vylozenia)
                    source_vylozenia = source
                    if source_vylozenia == None:
                        source_vylozenia = "vstup"
                    id_address = None
                    total_address = None
                    link = None
                    source = None
                    if source == None:
                        source = "vstup"
                    ##################################################  Pocitanie trasy        
                    vzdialenost, cas, cesta_link, source = ( 
                        pocitanie_trasy.spracovat_adresy(Adresa_Vyzdvyhnutia, Adresa_Vylozenia, 
                        Nadstavenia.Google_on_api, Nadstavenia.Googleapi)
                        )
                    print("cas-findal")
                    print(cas)
                    print(type(cas))
                    # Extrahujte hodiny a minúty pomocou regulárneho výrazu
                    try:
                         vysledok = re.findall(r'\d+', cas)
                     
                         pocet_prvkov = len(vysledok)
                     
                         if pocet_prvkov == 1:
                             minuty = int(vysledok[0])
                             celkove_minuty = minuty
                         else:
                             hodiny = int(vysledok[0])
                             minuty = int(vysledok[1])
                             celkove_minuty = hodiny * 60 + minuty
                     
                         cas_cesty = celkove_minuty
                         
                         print("cas_cesty")
                         print(cas_cesty)
                         print(type(cas_cesty))
                         
                    except:
                         cas_cesty = None
    
                    sources = source
                    if source == "Databaza":
                        source = "D"
                    if source == "Google API":
                        source = "A"
                    
                    if vzdialenost == None:
                        vzdialenost = "Km"
                                        
                    if cesta_link == None:
                        cesta_link = f"https://www.google.com/maps/dir/?api=1&origin={Adresa_Vyzdvyhnutia}&destination={Adresa_Vylozenia}&travelmode=car"
                        
    
                    telegram_message = (
                        "<b>" + Sofer + "</b>\n" + "<b>" + str(Cena) + " €      " + "<a href='" + cesta_link + "'>" + vzdialenost + "</a> </b>" +
                        "\n" + "<a href='" + start_link + "'>" + Adresa_Vyzdvyhnutia + "</a>\n ---------> \n" +
                        "<a href='" + ciel_link + "'>" + Adresa_vylozenia + "</a>\n" + Meno_zakaznika + "\n" + Nadstavenia.STROJ + source
                        )
                    Rozdiel = None
                    Kniha_jazd = (
                        str(Datum_prijatia) + " ; " + str(Cas_prijatia) + " ; " + str(Adresa_Vyzdvyhnutia) + " ; " +
                        str(Adresa_Vylozenia) + " ; " + str(Sofer) + " ; " + str(vzdialenost) + " ; " +
                        str(Cena) + " ; " + str(sources) 
                        )
                    if cas_cesty != None and Cena != "Preis":      
                        Rozdiel, Rozdiel_text = porovnanie.porovnanie(vzdialenost, cas_cesty, Cena, cas_prijatia, Datum_prijatia, Adresa_Vyzdvyhnutia, Adresa_Vylozenia, Sofer, Meno_zakaznika)
                    print("rozdiel telo")        
                    print(Rozdiel)
                    print(type(Rozdiel))
                    if Rozdiel != None:
                        Rozdiel = float(Rozdiel)
    
                    Dovod, Min_cena = podmienka.podmienka(driver, Kniha_jazd, Cena, Adresa_Vyzdvyhnutia, Adresa_Vylozenia, vzdialenost, Sofer, telegram_message, akcepte, Rozdiel)
    
                    if Cena == ("Preis"):
                        Cena = ("Undefiniert")
    
                    if Dovod == 'Prijate':
                        Dovod = ""
                    
                    if Dovod == "":
                        Posledna_zakazka = ( 
                        str(Aktualny_cas) + "  " + str(Sofer) + " " + str(Cena) + "€   " + vzdialenost + "\n"       + str(Adresa_Vyzdvyhnutia) + 
                        " \n        " + str(Adresa_Vylozenia) + "\n        Minimalna cena:" + str(Min_cena)
                        )
                    else:
                        pass
                    if Dovod == "" and Min_cena < 9:
                        Posledna_zakazka = ( 
                        Aktualny_cas + "  " + Sofer + " " + str(Cena) + "€   " + vzdialenost + "\n      " + Adresa_Vyzdvyhnutia + 
                        " \n        " + Adresa_Vylozenia 
                        )
                    else:
                        pass
                    if Dovod !="" and Dovod != None and Min_cena >= 7:
                        Posledna_zakazka = ( 
                            Aktualny_cas + "  " + Sofer + " " + str(Cena) + "€   " + vzdialenost + "\n      " + Adresa_Vyzdvyhnutia + 
                            " \n        " + Adresa_Vylozenia + "\n      " + str(Dovod) + "\n" + "           Minimalna cena:" + str(Min_cena) 
                            )
                    else:
                        pass
                    
                    
        except StaleElementReferenceException:
            print("StaleElementReferenceException: Waiting for 5 seconds and then retrying...")
            time.sleep(1)
            driver.refresh()
            time.sleep(2)
            continue  # Pokračovat od začátku smyčky
                    
                    
                    
