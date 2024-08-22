#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:09:51 2023
@author: priwi
"""
import Nadstavenia
import Email

def porovnanie (vzdialenost, cas_cesty, Cena, cas_prijatia, Datum_prijatia, Adresa_Vyzdvyhnutia, Adresa_Vylozenia, Sofer, Meno_zakaznika):

                # Uprava jednotiek  pre vypocet
    vzdialenost = vzdialenost.replace("km", "").replace("Km", "").replace(",", ".").replace("m", "")
    vzdialenost = float(vzdialenost)
                    # pozor je za potreby prepocitanie pri dlhych trasach aby pociatalo na minuty 
    hodiny = cas_cesty // 60
    minuty = cas_cesty % 60

    # Vytvorte reťazec s hodinami a minutami vo formáte "hodiny.minuty"
    cas_cesty = f"{hodiny}.{minuty:02}"
    cas_cesty = float(cas_cesty)

    Rozdiel = 0
    Rozdiel_text = " "
    Prepocet_cena_km = Nadstavenia.cena_km * vzdialenost
    Prepocet_cena_cas = Nadstavenia.cena_cas * cas_cesty
    Cena_uber_zakaznik = Nadstavenia.nastup + (Nadstavenia.cena_km * vzdialenost) + (Nadstavenia.cena_cas * cas_cesty)
    Nasa_cena = Cena_uber_zakaznik * 0.7025
    Cena_uber_zakaznik = round(Cena_uber_zakaznik, 2)
    Nasa_cena = round(Nasa_cena, 2)

    print("Pred porovnavynym")
    print("Nasa_cena")
    print(Nasa_cena)
    print(type(Nasa_cena))

    print("Cena")
    print(Cena)
    print(type(Cena))

    # Vykonajte príslušné kroky pre tento prípad
    if Cena != "Preis" and Cena != None:
        if Cena < Nasa_cena:
            print("Nasacena")
            print(type(Nasa_cena))
            print(Cena)
            print(type(Cena))
            Rozdiel = Nasa_cena - Cena
            Rozdiel = round(Rozdiel, 2)
            Uber_gebuhr = Cena_uber_zakaznik * 0.2975
            Uber_gebuhr = round(Uber_gebuhr, 2)
            print(Rozdiel)
            print(type(Rozdiel))
            print("ZLA CENA: cena je nižšia o: " + str(Rozdiel) + "€")
            
            Rozdiel_text = ("ZLA CENA: cena je nižšia o: " + str(Rozdiel) + "€")

            Body =  (
                    f"""
                    <html>
                    <body>
                    <p>Auftrag {Datum_prijatia}, {cas_prijatia}, Abholung: {Adresa_Vyzdvyhnutia} Zieladresse: {Adresa_Vylozenia}, Preis: {Cena} €, Kunde: {Meno_zakaznika}, Fahrer: {Sofer}</p>
                    <p>Leider diese Preis stimmt nicht.</p>
                    <p>Der aktuelle Abstand zwischen den Adressen beträgt: {vzdialenost} Km</p>
                    <p>Zwischen den Adressen ist die Reisezeit in der aktuellen Zeit: {cas_cesty} St.</p>
                    <p>Übervoreingestellte Preise:</p>
                    <ul>
                    <li>Einsteg: {Nadstavenia.nastup} €</li>
                    <li>Preis pro Km: {Nadstavenia.cena_km} €</li>
                    <li>Zeit: {Nadstavenia.cena_cas} €</li>
                    <li></li>
                    <li>Preis berechnung: </li>
                    <li>Einsteg: {Nadstavenia.nastup} €</li>
                    <li>KM: {vzdialenost} x {Nadstavenia.cena_km} = {Prepocet_cena_km} €</li>
                    <li>Zeit: {cas_cesty} x {Nadstavenia.cena_cas}  = {Prepocet_cena_cas} €</li>
                    <li>Preis für Kunde: {Cena_uber_zakaznik} €</li>
                    </ul>
                    <p>Abzüge:</p>
                    <ul>
                    <li>29.75% Übergebühr = {Uber_gebuhr} €</li> 
                    <li>Preis nach dem gebuhr abzüg: {Nasa_cena} € </li>
                    <li>In diesem Fall ist die Differenz: {Rozdiel} €</li>
                    </ul>
                    <p>Aus diesen Gründen bitte ich Uber, die Differenz {Rozdiel} € zu zahlen! Bis Nachste Montag, Muss in rechnung extra steth! </p>
                    <p>Weiter ich informieren Der UBER und ENNO, dass Sie im Dispatch keine Informationen teilen, als:</p>
                    <ul>
                    <li>Produkt: X, Premium, XL, ....</li>
                    <li>Informationen zum dynamischen Preis.</li>
                    <li>Kennzeichen des Fahrzeugs</li>
                    </ul>
                    <p>Dies macht eine Neuberechnung und Kontrolle der Preise unmöglich. Wie hoch ist Ihre Fehlerquote bei einem hohen Prozentsatz? Ich bitte Sie, diese Angaben zu vervollständigen</p>
                    <p>Zurzeit sind auch solche Aufträge angekommen. Wenn keine Verbesserung kommt bis in 1 Monat kommt, dann wurde solche Aufträge ablehnen.</p>
                    <br /><br /><em>Mit freundlichen Grüßen<br />Team Premium Limo Service GMBH</em><br />
                    <div style="text-size-adjust: none !important; -ms-text-size-adjust: none !important; -webkit-text-size-adjust: none !important;">
                      <p style="font-family: Helvetica,Arial,sans-serif; font-size: 10px; line-height: 12px; margin-bottom: 10px;"> 
                        <a style="text-decoration: none;" href="http://www.premium-limo-service.com">
                        	<img src="https://premium-limo-service.com/LOGO/Logo_email.png" alt="Premium Limo Service GmbH" width="120" border="0">
                        </a> 
                  
                      </p>               
                      <p style="font-family: Helvetica,Arial,sans-serif; font-size: 10px; line-height: 12px; color: rgb(33, 33, 33); margin-bottom: 10px;">  
                           <span style="font-weight: bold; color: rgb(33, 33, 33); display: inline; font-size:11px;">Premium Limo Service HMBH</span> <br />    
                               <span style="color: rgb(0, 0, 0); display: inline;">Team Premium Limo Service GMBH</span> <br /> 
                               <a href="mailto:info@premium-limo-service.com" style="color: rgb(71, 124, 204); text-decoration: none; display: inline;">peter@premium-limo-service.com</a>
                        <span style="display: inline;"> / </span>
                              <span style="color: rgb(33, 33, 33); display: inline;">+49 176 8148 0763</span> 
                      </p>            
                      <p style="font-family: Helvetica,Arial,sans-serif; font-size: 10px; line-height: 12px; margin-bottom: 10px;">   
                                <span style="font-weight: bold; color: rgb(33, 33, 33); display: inline; font-size:11px;">Premium Limo Service GmbH</span><br />
                           <span style="color: rgb(33, 33, 33); display: inline;">Im Wiegenfeld 4</span><br />
                           <span style="color: rgb(33, 33, 33); display: inline;">85570 Markt Schwaben</span><br />
                                        <a href="http://www.premium-limo-service.com" style="color: rgb(71, 124, 204); text-decoration: none; display: inline;">www.premium-limo-service.com</a><br />
                      </p>            
                      <p style="font-family: Helvetica,Arial,sans-serif; font-size: 10px; line-height: 12px; margin-bottom: 10px;">   
                             <a href="Premium Limo Service"><img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.qBF304Itw7ZGuLTDtdtr0QHaHa%26pid%3DApi&f=1" alt="Facebook" width="20" border="0"></a>
                             <a href="premium_limo_service"><img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.YxlwFVJxJKTy88hZ0NWvswHaHa%26pid%3DApi&f=1" alt="Instagram" width="20" border="0"></a>
                                    <a href="+49 176 8148 0763"><img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.yLJwv_Tuq7mytXbF1TF6OAHaHa%26pid%3DApi&f=1" alt="Twitter" width="20" border="0"></a>
                                                <a href="+49 176 8148 0763"><img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.wFWRVqVsMXhnyoYtiKmdZwHaHa%26pid%3DApi&f=1" alt="Youtube" width="20" border="0"></a>
                                  
                      </p>
                    </div>
                    </body>
                    </html>
                    """
                    )
            
            Email.send_email(Body)
            print ("Email poslany!")
    print("Po porovnany")
    print("Nasa_cena")
    print(Nasa_cena)
    print(type(Nasa_cena))

    print("Cena")
    print(Cena)
    print(type(Cena))    
    return Rozdiel, Rozdiel_text
