#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:09:51 2023
@author: priwi
"""

from selenium.webdriver.common.by import By
import Nadstavenia
import spravy
import time
import importlib
from datetime import datetime
from dateutil.parser import parse
import datetime
# #podmienka.podmienka(driver, Kniha_jazd, Cena, Adresa_Vyzdvyhnutia, Adresa_Vylozenia, vzdialenost, Sofer, telegram_message, akcepte, Rozdiel)

def podmienka(driver, Kniha_jazd, cena, adresa_vyzdvyhnutia, adresa_vylozenia, vzdialenost, sofer, telegram_message, akcepte, Rozdiel):

    importlib.reload(Nadstavenia)
    importlib.reload(spravy)
    print("podmienka")
    print(cena)

    if Rozdiel != None:
        if Rozdiel > 0:
            Rozdiel = (f"preis ist {Rozdiel} € niedrige als grundpreis")
    Dovod = None
    sofer = str(sofer)
    aktualny_cas = datetime.datetime.now()
    if Nadstavenia.Min_cena == None:
        Nadstavenia.Min_cena = 1  
    Min_cena = float(Nadstavenia.Min_cena)
    adresa_vyzdvyhnutia = str(adresa_vyzdvyhnutia)
    PSC_vyzdvyhnutia = Nadstavenia.PSC_vyzdvyhnutia
    adresa_vylozenia = str(adresa_vylozenia)
    PSC_vylozenia = Nadstavenia.PSC_cielu
    vzdialenost = vzdialenost.replace("km", "").replace("Km", "").replace(" ", "").replace(",", ".").replace("m", "")
    if vzdialenost == "" or vzdialenost == "Km":
        vzdialenost = None 
    if vzdialenost != None:
        vzdialenost = str(vzdialenost)  # Prevod hodnoty na reťazec
        # vzdialenost = vzdialenost.replace("km", "").replace("Km", "").replace(" ", "").replace(",", ".").replace("m", "")
        vzdialenost = float(vzdialenost)
        if vzdialenost != '':
            vzdialenost = float(vzdialenost)
        else:
            vzdialenost = None
            
    schedule_time_on = Nadstavenia.schedule_time_on
        
    Min_vzdialenost = float(Nadstavenia.Min_km)
    Max_vzdialenost = float(Nadstavenia.Max_km)
    sofer = str(sofer)
    Max_cena = float(Nadstavenia.Max_cena)
    Vyluceny_sofer = str(Nadstavenia.Vyluceny_sofer)
    #Vyluceny_sofer_casovka = str(Nadstavenia.Vyluceny_sofer_casovka)

    aktualny_cas = datetime.datetime.now()
    den_v_tyzdni = aktualny_cas.strftime("%A").lower()

    print("Aktuálny čas:", aktualny_cas)
    print("Deň v týždni:", den_v_tyzdni)

    print("Pred casovkou")
    print(cena)
    print("min_cena")
    print(Min_cena)
    
    #ercent_value, schedule_time_on = pocitanie_percent.analyze_and_update_schedule(Nadstavenia.schedule_time_on)
    
    if schedule_time_on == 1:
        if den_v_tyzdni in Nadstavenia.Casovy_rozvrh:
            hodnoty = Nadstavenia.Casovy_rozvrh[den_v_tyzdni]
            for cas, hodnota_ceny in hodnoty.items():
                casy = cas.split("-")
                zaciatok = parse(casy[0]).time()
                koniec = parse(casy[1]).time()
                if zaciatok <= aktualny_cas.time() <= koniec:
                    Min_cena = hodnota_ceny
                    break
        else:
            # Případ, kdy pro aktuální den není žádný časový rozvrh definován
            Min_cena = Nadstavenia.Min_cena
            
    print("Po casovke")
    print(cena)
    print("Min_cena")
    print(Min_cena)
            
    print("pred soferom ")
    if Nadstavenia.Zvyhodneny_sofer_on == 1:
        if cena != None and cena != "Preis":
            if sofer in Nadstavenia.Zvyhodneny_sofer:
                Min_cena = Nadstavenia.Zvyhodneny_sofer[sofer]
                Min_cena = float(Min_cena)
                print(Min_cena)
    
#    if Nadstavenia.Vyluceny_sofer_casovka_on == 1:
#        if sofer in Vyluceny_sofer_casovka:
#            Min_cena = float(1)
    
    print("rozdiel podmienka")
    print(Rozdiel)
    print(cena)
    print("pred podmienkamy" + str(cena))
    if Rozdiel == None or Rozdiel == float(0):
        if cena != "Preis" and  cena != None and Nadstavenia.Min_cena >= 0:
            print("if cena is not None and cena !=  and Nadstavenia.Min_cena > 1:")
            if (cena) > (Min_cena):
                print("if float(cena) > Min_cena:")
                if not any(str(PSC_V) in adresa_vyzdvyhnutia for PSC_V in PSC_vyzdvyhnutia):  # Vyzdvihnutie
                    print("Vyzdvyhnutie")
                    if not any(str(PSC_VY) in adresa_vylozenia for PSC_VY in PSC_vylozenia):  # Vyloženie
                        print("Volzenie")
                        if vzdialenost != None:
                            print("KM")
                            if  Min_vzdialenost < vzdialenost < Max_vzdialenost :  # Vzdialenosť
                                print("Vzdialenost")
                                if sofer in Vyluceny_sofer:
                                    print(f"Vylúčený: {sofer}")
                                    Dovod = 'Prijate'
                                    print(akcepte)
                                    akcepte.click()
                                    Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                                    with open("Kniha_objednavok.txt", "a") as file:
                                        file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                        spravy.me_send_to_telegram(telegram_message + "\n" + Dovod)
                                else:   # if sofer in Vyluceny_sofer:
                                    print("Meno Potvrdzovacieho tlacidla")
                                    print(akcepte)
                                    akcepte.click()
                                    print("potvrdena zakazka")
                                    Dovod = "Prijate"      
                                    print(Dovod)
                                    print("vytvorenie knihy jazd")
                                    Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod  + " ; " + str(Rozdiel)
                                    print("pred zapisom knihy jazd")
                                    with open("Kniha_objednavok.txt", "a") as file:
                                        file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                    print("po zapise knihy jazd")
                                    print("pred poalsanim telegramov")
                                    spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                    spravy.send_to_telegram_with_timer(telegram_message)                                           
                            else:   # if vzdialenost > Min_vzdialenost:  # Vzdialenosť
                                if vzdialenost > Max_vzdialenost:
                                    prepocet_cena = vzdialenost*float(1.3)
                                    if cena >= prepocet_cena:
                                        print("Prekrocena Max vzdialenost + dodrzana cena")
                                        akcepte.click()
                                        Dovod = "Prekrocena Max vzdialenost - dodrzana cena"        
                                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod  + " ; " + str(Rozdiel)
                                        with open("Kniha_objednavok.txt", "a") as file:
                                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                        spravy.send_to_telegram_with_timer(telegram_message)
                                    else:
                                        print("Prekrocena Max vzdialenost nedodrzana cena")
                                        Dovod = "Prekrocena Max vzdialenost nedodrzana cena"
                                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod  + " ; " + str(Rozdiel)
                                        with open("Kniha_objednavok.txt", "a") as file:
                                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                else:
                                    print("Vzdialenosť Km je mimo povoleného rozsahu.")
                                    Dovod = f"Nedosiahnuta vzdialenosť min {Min_vzdialenost} max {Max_vzdialenost}  Km."
                                    Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod  + " ; " + str(Rozdiel)
                                    with open("Kniha_objednavok.txt", "a") as file:
                                        file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                    spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                
                                
                        else:   # if vzdialenost != None:
                            Dovod = 'Prijate'
                            print(akcepte)
                            akcepte.click()
                            Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                            with open("Kniha_objednavok.txt", "a") as file:
                                file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                            spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                            spravy.send_to_telegram_with_timer(telegram_message)
                                
                            if sofer in Vyluceny_sofer:
                                print(f"Vylúčený: {sofer}")
                                Dovod = 'Prijate'
                                print(akcepte)
                                akcepte.click()
                                Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                                with open("Kniha_objednavok.txt", "a") as file:
                                    file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                spravy.me_send_to_telegram(telegram_message + "\n" + Dovod)
                            else:   # if sofer in Vyluceny_sofer:
                                print(akcepte)
                                akcepte.click()
                                Dovod = "Prijate"        
                                Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                                with open("Kniha_objednavok.txt", "a") as file:
                                    file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                
                    else:   # if not any(str(PSC_VY) in adresa_vylozenia for PSC_VY in PSC_vylozenia):  # Vyloženie
                        # if Nadstavenia.Oktoberfest == 1: 
                        #     if (cena) > (50):
                        #         print(akcepte)
                        #         akcepte.click()
                        #         Dovod = "Prijate"        
                        #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        #         with open("Kniha_objednavok.txt", "a") as file:
                        #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        #         spravy.send_to_telegram_with_timer(telegram_message)  
                        #     elif (vzdialenost) > (30):
                        #         print(akcepte)
                        #         akcepte.click()
                        #         Dovod = "Prijate"        
                        #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        #         with open("Kniha_objednavok.txt", "a") as file:
                        #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        #         spravy.send_to_telegram_with_timer(telegram_message)  
                        #     else:
                        #         nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                        #         nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                        #         print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                        #         Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                        #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        #         with open("Kniha_objednavok.txt", "a") as file:
                        #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        # else:
                        if (cena) > (float(50)):  
                            print(akcepte)
                            akcepte.click()
                            Dovod = "Prijate zakazane PSC cena > 50€"        
                            Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                            with open("Kniha_objednavok.txt", "a") as file:
                                file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                            spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                            spravy.send_to_telegram_with_timer(telegram_message) 
                        
                        elif (vzdialenost) > (float(30)):
                            print(akcepte)
                            akcepte.click()
                            Dovod = "Prijate zakazane PSC vzdilenost > 30Km"        
                            Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                            with open("Kniha_objednavok.txt", "a") as file:
                                file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                            spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                            spravy.send_to_telegram_with_timer(telegram_message) 
                            
                        else:
                            nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                            nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                            print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                            Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                            Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                            spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                            with open("Kniha_objednavok.txt", "a") as file:
                                file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                    
                else:   # if not any(str(PSC_V) in adresa_vyzdvyhnutia for PSC_V in PSC_vyzdvyhnutia):  # Vyzdvihnutie
                    # if Nadstavenia.Oktoberfest == 1: 
                    #     if (cena) > (50):
                    #         print(akcepte)
                    #         akcepte.click()
                    #         Dovod = "Prijate"        
                    #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                    #         with open("Kniha_objednavok.txt", "a") as file:
                    #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                    #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                    #         spravy.send_to_telegram_with_timer(telegram_message)  
                    #     elif (vzdialenost) > (30):
                    #         print(akcepte)
                    #         akcepte.click()
                    #         Dovod = "Prijate"        
                    #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                    #         with open("Kniha_objednavok.txt", "a") as file:
                    #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                    #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                    #         spravy.send_to_telegram_with_timer(telegram_message)  
                    #     else:
                    #         nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                    #         nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                    #         print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                    #         Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                    #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                    #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                    #         with open("Kniha_objednavok.txt", "a") as file:
                                # file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                    # else:
                    if (cena) > (float(50)):  
                        print(akcepte)
                        akcepte.click()
                        Dovod = "Prijate zakazane PSC cena > 50€"        
                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        with open("Kniha_objednavok.txt", "a") as file:
                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        spravy.send_to_telegram_with_timer(telegram_message) 
                    
                    elif (vzdialenost) > (float(30)):
                        print(akcepte)
                        akcepte.click()
                        Dovod = "Prijate zakazane PSC vzdilenost > 30Km"        
                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        with open("Kniha_objednavok.txt", "a") as file:
                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        spravy.send_to_telegram_with_timer(telegram_message) 
                        
                    else:
                        nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                        nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                        print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                        Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        with open("Kniha_objednavok.txt", "a") as file:
                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
            else:   # if (cena) > (Min_cena):
                print(f"Cena {cena} je mimo povoleného rozsahu.")
                Dovod = f"Cena {cena} je mimo povoleného rozsahu."
                Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                with open("Kniha_objednavok.txt", "a") as file:
                    file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
        else:   # if cena != "Preis" and  cena != None and Nadstavenia.Min_cena >= 0:
            if cena == "Preis":
                Min_vzdialenost = float(30)
                if not any(str(PSC_V) in adresa_vyzdvyhnutia for PSC_V in PSC_vyzdvyhnutia):  # Vyzdvihnutie
                    if not any(str(PSC_VY) in adresa_vylozenia for PSC_VY in PSC_vylozenia):  # Vyloženie
                        if vzdialenost is not None and vzdialenost != "" and vzdialenost != 0 and vzdialenost != "Km" and vzdialenost != "km":
                            if vzdialenost > Min_vzdialenost:  # Vzdialenosť
                                if sofer in Vyluceny_sofer:
                                    print(f"Vylúčený: {sofer}")
                                    Dovod = 'Prijate'
                                    print(akcepte)
                                    akcepte.click()
                                    Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                                    with open("Kniha_objednavok.txt", "a") as file:
                                        file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                else:
                                    if all(vyluceny_sofer_check not in sofer for vyluceny_sofer_check in Vyluceny_sofer):  # Vylúčený šofér
                                        print(akcepte)
                                        akcepte.click()
                                        Dovod = "Prijate"            
                                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                                        with open("Kniha_objednavok.txt", "a") as file:
                                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                        spravy.send_to_telegram_with_timer(telegram_message)
                                    else:  # Obmedzenie vzdialenosti
                                        print(f"Vzdialenosť {vzdialenost} Km je mimo povoleného rozsahu.")
                                        Dovod = f"Nedosiahnuta vzdialenosť {Max_vzdialenost} Km."
                                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                        with open("Kniha_objednavok.txt", "a") as file:
                                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                            else:   # if vzdialenost > Min_vzdialenost:  # Vzdialenosť
                                if vzdialenost > Max_vzdialenost:
                                    prepocet_cena = vzdialenost*float(1.3)
                                    if cena >= prepocet_cena:
                                        print("Prekrocena Max vzdialenost ++ dodrzana cena")
                                        akcepte.click()
                                        Dovod = "Prekrocena Max vzdialenost ++ dodrzana cena"        
                                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod  + " ; " + str(Rozdiel)
                                        with open("Kniha_objednavok.txt", "a") as file:
                                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                        spravy.send_to_telegram_with_timer(telegram_message)
                                    else:
                                        print("Prekrocena Max vzdialenost nedodrzana cena")
                                        Dovod = "Prekrocena Max vzdialenost nedodrzana cena"
                                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod  + " ; " + str(Rozdiel)
                                        with open("Kniha_objednavok.txt", "a") as file:
                                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                                else:
                                    print("Vzdialenosť Km je mimo povoleného rozsahu.")
                                    Dovod = f"Nedosiahnuta vzdialenosť min {Min_vzdialenost} max {Max_vzdialenost}  Km."
                                    Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod  + " ; " + str(Rozdiel)
                                    with open("Kniha_objednavok.txt", "a") as file:
                                        file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                    spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                            
                    else:   # if not any(str(PSC_VY) in adresa_vylozenia for PSC_VY in PSC_vylozenia):  # Vyloženie
                        # if Nadstavenia.Oktoberfest == 1: 
                        #     if (cena) > (50):
                        #         print(akcepte)
                        #         akcepte.click()
                        #         Dovod = "Prijate"        
                        #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        #         with open("Kniha_objednavok.txt", "a") as file:
                        #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        #         spravy.send_to_telegram_with_timer(telegram_message)  
                        #     elif (vzdialenost) > (30):
                        #         print(akcepte)
                        #         akcepte.click()
                        #         Dovod = "Prijate"        
                        #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        #         with open("Kniha_objednavok.txt", "a") as file:
                        #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        #         spravy.send_to_telegram_with_timer(telegram_message)  
                        #     else:
                        #         nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                        #         nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                        #         print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                        #         Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                        #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        #         with open("Kniha_objednavok.txt", "a") as file:
                        #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        # else:
                        if (cena) > (float(50)):  
                            print(akcepte)
                            akcepte.click()
                            Dovod = "Prijate zakazane PSC cena > 50€"        
                            Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                            with open("Kniha_objednavok.txt", "a") as file:
                                file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                            spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                            spravy.send_to_telegram_with_timer(telegram_message) 
                        
                        elif (vzdialenost) > (float(30)):
                            print(akcepte)
                            akcepte.click()
                            Dovod = "Prijate zakazane PSC vzdilenost > 30Km"        
                            Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                            with open("Kniha_objednavok.txt", "a") as file:
                                file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                            spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                            spravy.send_to_telegram_with_timer(telegram_message) 
                            
                        else:
                            nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                            nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                            print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                            Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                            Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                            spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                            with open("Kniha_objednavok.txt", "a") as file:
                                file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                                
                else:   # if not any(str(PSC_V) in adresa_vyzdvyhnutia for PSC_V in PSC_vyzdvyhnutia):  # Vyzdvihnutie
                    # if Nadstavenia.Oktoberfest == 1: 
                    #     if (cena) > (50):
                    #         print(akcepte)
                    #         akcepte.click()
                    #         Dovod = "Prijate"        
                    #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                    #         with open("Kniha_objednavok.txt", "a") as file:
                    #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                    #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                    #         spravy.send_to_telegram_with_timer(telegram_message)  
                    #     elif (vzdialenost) > (30):
                    #         print(akcepte)
                    #         akcepte.click()
                    #         Dovod = "Prijate"        
                    #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                    #         with open("Kniha_objednavok.txt", "a") as file:
                    #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                    #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                    #         spravy.send_to_telegram_with_timer(telegram_message)  
                    #     else:
                    #         nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                    #         nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                    #         print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                    #         Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                    #         Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                    #         spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                    #         with open("Kniha_objednavok.txt", "a") as file:
                    #             file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                    # else:
                    if (cena) > (float(50)):  
                        print(akcepte)
                        akcepte.click()
                        Dovod = "Prijate zakazane PSC cena > 50€"        
                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        with open("Kniha_objednavok.txt", "a") as file:
                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        spravy.send_to_telegram_with_timer(telegram_message) 
                    
                    elif (vzdialenost) > (float(30)):
                        print(akcepte)
                        akcepte.click()
                        Dovod = "Prijate zakazane PSC vzdilenost > 30Km"        
                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        with open("Kniha_objednavok.txt", "a") as file:
                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        spravy.send_to_telegram_with_timer(telegram_message) 
                        
                    else:
                        nepovolene_psc_v = [str(prvok) for prvok in PSC_vylozenia if str(prvok) in adresa_vylozenia]
                        nepovolene_psc_v_str = ', '.join(str(psc) for psc in nepovolene_psc_v)
                        print(f"Adresa vyloženia obsahuje zakázané PSC: {nepovolene_psc_v_str}")
                        Dovod = f"Zakázané PSC {nepovolene_psc_v_str}"
                        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod + " ; " + str(Rozdiel)
                        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)
                        with open("Kniha_objednavok.txt", "a") as file:
                            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
                            
            else:   # (cena) > (Min_cena):
                pass                     
    else:   # if Rozdiel != None and Rozdiel > 0:
        Dovod = "Cena pod garantovanu uroven!!"        
        Kniha_jazd_konecna = Kniha_jazd + " ; " + Dovod  + " ; " + str(Rozdiel)
        with open("Kniha_objednavok.txt", "a") as file:
            file.write(Kniha_jazd_konecna + "\n")  # Zápis dát do súboru
        spravy.me_send_to_telegram(telegram_message + "\n" +  Dovod)  
            
    return Dovod, Min_cena
