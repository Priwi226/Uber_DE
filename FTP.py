#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 22:31:05 2023

@author: priwi
"""
import ftplib
import Nadstavenia
import importlib
import datetime
import time


 ################################################################# prekopirovanie suboru na ftp
def reload_modules():
    importlib.reload(Nadstavenia) 

def FTP_write():
    while True:
        importlib.reload(Nadstavenia)
        # Vytvoríme pripojenie k FTP serveru
        ftp = ftplib.FTP(Nadstavenia.FTP_NAME)
        ftp.login(Nadstavenia.FTP_MENO , Nadstavenia.FTP_HESLO)

        # Prepneme sa do adresára "Python"
        directory_name = "Python"
        ftp.cwd(directory_name)

        # Získaj aktuálny čas
        aktuality_cas = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Vytvor súbor "Uber_clicker" v aktuálnom priečinku
        file_name = "Uber_clicker.txt"
        with open(file_name, "w") as file:
            file.write(aktuality_cas)

        # Nakopíruj súbor na FTP server
        with open(file_name, "rb") as file:
            ftp.storbinary(f"STOR {file_name}", file)

        # Ukončenie pripojenia k FTP serveru
        ftp.quit()
        print("writer")
        time.sleep(60)
###########################################################################
def databaza_copy():

    subor_databazy = "Databaza/databaza.db"
    cesta_k_suboru = "data/" + subor_databazy
 
    ftp = ftplib.FTP(Nadstavenia.FTP_NAME , Nadstavenia.FTP_MENO , Nadstavenia.FTP_HESLO )

    # Prechod do adresára "Python" na FTP serveri
    ftp.cwd("Python")

    # Nahranie súboru na FTP server
    with open(cesta_k_suboru, "rb") as file:
        ftp.storbinary("STOR " + subor_databazy, file)

    # Odpojenie z FTP servera
    ftp.quit()

###########################################################################

def databaza_copy():
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == "01:43":
            # Vytvoříme připojení k FTP serveru
            ftp = ftplib.FTP(Nadstavenia.FTP_NAME)
            ftp.login(Nadstavenia.FTP_MENO, Nadstavenia.FTP_HESLO)

            # Přepneme se do adresáře "Databaza" na FTP serveru
            directory_name = "Databaza"
            ftp.cwd(directory_name)

            file_name = "data/gmp.db"  # Upravte cestu a název souboru podle vašich potřeb

            # Kopírování souboru na FTP
            with open(file_name, "rb") as file:
                ftp.storbinary(f"STOR gmp.db", file)

            # Kopírování souboru na FTP
            with open(file_name, "rb") as file:
                ftp.storbinary(f"STOR gmp.db", file)

            ftp.quit()
            print("Databaza ulozena na FTP server")
        time.sleep(60)  # Počká 60 sekund před dalším zkontrolováním času

