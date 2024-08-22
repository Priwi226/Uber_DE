#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:09:51 2023
@author: priwi
"""

from selenium.webdriver.common.by import By
import Nadstavenia
import spravy
import datetime
import time
import importlib

def podmienka2(driver, Kniha_jazd, cena, adresa_vyzdvyhnutia, adresa_vylozenia, vzdialenost, sofer, telegram_message, element_akcept):

    importlib.reload(Nadstavenia)

    Min_cena = float(Nadstavenia.Min_cena)
    adresa_vyzdvyhnutia = str(adresa_vyzdvyhnutia)
    PSC_vyzdvyhnutia = Nadstavenia.PSC_vyzdvyhnutia
    adresa_vylozenia = str(adresa_vylozenia)
    PSC_vylozenia = Nadstavenia.PSC_cielu
    vzdialenost = vzdialenost.replace("km", "").replace("Km", "")
    cena = cena.replace("€", "").replace (" ", "").replace(",", ".")
    if vzdialenost != '':
        vzdialenost = float(vzdialenost)
    Max_vzdialenost = float(Nadstavenia.Max_km)
    sofer = str(sofer)
    vyl_sofer = Nadstavenia.Vyluceny_sofer
    Min_cena = float(Min_cena)
    Max_cena = float(Nadstavenia.Max_cena)
    Vyluceny_sofer = Nadstavenia.Vyluceny_sofer
    now = datetime.datetime.now()
    den_v_tyzdni = now.strftime("%A").lower()
    
    if cena is not None and cena != "undefined":
        if float(cena) > Min_cena:
            print("presiel") 
            if not any(str(PSC_V) in adresa_vyzdvyhnutia for PSC_V in PSC_vyzdvyhnutia):  # Vyzdvihnutie
                if not any(str(PSC_VY) in adresa_vylozenia for PSC_VY in PSC_vylozenia):  # Vyloženie
                    if vzdialenost is not None and vzdialenost != "" and vzdialenost != 0 and vzdialenost != "Km" and vzdialenost != "km":
                        if vzdialenost < Max_vzdialenost:  # Vzdialenosť
                            if sofer in Vyluceny_sofer:
                                print(f"Vylúčený: {sofer}")
                                Dovod = 'Prijaté'
                                time.sleep(8)
                                element_akcept.click()
                                Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod
                                with open("Kniha_objednavok.txt", "a") as file:
                                    file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                spravy.me_send_to_telegram(telegram_message)
                            else:
                                if all(vyluceny_sofer_check not in sofer for vyluceny_sofer_check in Vyluceny_sofer):  # Vylúčený šofér
                                    Prijatie_zakazky = driver.find_element(By.XPATH, "//button[@data-baseweb='button']")
                                    Prijatie_zakazky.click()
                                    Dovod = "Prijaté"
                                    Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod
                                    with open("Kniha_objednavok.txt", "a") as file:
                                        file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                    spravy.me_send_to_telegram(telegram_message)
                                    spravy.send_to_telegram_with_timer(telegram_message)
                                else:  # Obmedzenie vzdialenosti
                                    print(f"Vzdialenosť {vzdialenost} Km je mimo povoleného rozsahu.")
                                    Dovod = f"Prekročená vzdialenosť {Max_vzdialenost} Km."
                                    Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod
                                    with open("Kniha_objednavok.txt", "a") as file:
                                        file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        else:
                            pass
                else:  # PSC vyloženia
                    nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                    nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                    print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                    Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                    Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod
                    with open("Kniha_objednavok.txt", "a") as file:
                        file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
            else:  # PSC vyzdvihnutia
                nepovolene_psc = [str(prvok) for prvok in PSC_vyzdvyhnutia if str(prvok) in adresa_vyzdvyhnutia]
                nepovolene_psc_str = ', '.join(str(psc) for psc in nepovolene_psc)
                print(f"Adresa vyzdvihnutia obsahuje zakázané PSC: {nepovolene_psc_str}")
                Dovod = f"Zakázané PSC {nepovolene_psc_str}"
                Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod
                with open("Kniha_objednavok.txt", "a") as file:
                    file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
        else:  # Cena
            print(f"Cena {cena} je mimo povoleného rozsahu.")
            Dovod = f"Cena {cena} je mimo povoleného rozsahu."
            Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod
            with open("Kniha_objednavok.txt", "a") as file:
                file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
    else:
        pass
