#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 07:38:28 2023

@author: priwi
"""





nastup = (4*0.7)        # 30%
cena_km = (1.18*0.7)    # 30%
cena_cas = (0.30*0.7)   # 30%


Prehliadac_on = 1 # 1 spusteny prehliadac 
#Google_on_api = 1 if dnes % 2 == 0 else 0 #kazdy parny den
Google_on_api = 1 #### 1 zapnut
schedule_time_on = 0
Zvyhodneny_sofer_on = 1 # 1 = zapnute
Vyluceny_sofer_casovka_on = 0 # 1 = zapnute 

KNIHA_JAZD = 1  # 0 vypnute

Oktoberfest = 0

###         Podmienky
Min_cena = 0
Max_cena = 100000 
Min_km = 0
Max_km = 100

###################################### 
A = Alianz = [80939, 89451, 23665, ]
M = Messe =  [81829, 81823, 85609]
L = Lilienalle = [80939]
O = Olympia = ["Spiridon-Louis-Ring", "BMW", "Lerchenauer"]
OO = Oktoberfest = [81373, 80339, 80336, 80337, 80335, "Hans-Fischer-Stra"
                    , "Theresienwiese", "Gotheplatz", "Oktoberfest", "Wiesn"]
PSC_vyzdvyhnutia = ()   # POUZIVAJ +
PSC_cielu = ()



######################################################
Vyluceny_sofer = ["Pet", "Jozko"]

Zvyhodneny_sofer = {
    "Per": 45,
    "Nikol": 1,
    "Fare": 1,
    }


###         Stroj
STROJ = ("Master")

###         Prihlasovanie na stranku
MENO = ("Email")
HESLO = ("Passwort")

Odmlka = int(5)

###         Telegram Data
Telegram_api_Token_uber = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
Telegram_api_Token_kiwi = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
Telegram_miestnost_kiwi = ("xxxxxxxxx")  #---- KIWI
Telegram_miestnost_uber = ("xxxxxxxxxxxxxx")  #---- Auftrags
Telegram_miestnost_ja = ("xxxxxxxxxxxxxxxx")  #---- Uber zakazky
URL = ("f'https://api.telegram.org/bot{apiToken}/sendMessage'")
Telegram_mazanie = "300"


###         SMS data
Sms_kluc = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

##FTP Nadstavenia 
Download_add = ("/home/priwi/Stiahnuté")

FTP_NAME = ("xxx.xxx.xxx.xxx")
FTP_MENO = ("Name")
FTP_HESLO = ("passwort")
FTP_Cesta = ("/Python")
FTP_SUBOR = ("Uber_clicker.txt")
FTP_cas = 63

Nazov_subory =("driver_performance.csv")

####        Definovanie slov
Povodny_nazov_obsahuje = ("Driver Quality")
slovo = ("Kvalita vodiča")



###### Email nadstavenia
SMTP = ("smtp")
IMAP = ("imap")
Email_meno = ("aaaa@aaa.aaa")
Email_heslo = ("Passwort")
Odosielatel = ("Absender")
Predmet = ("[SMSFW] New text.........................")


####   Google API
Googleapi =  ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

Casovy_rozvrh = {
    "monday": {
        '04:00-05:00': 13,
        '05:00-07:00': 12,
        '07:00-08:00': 10,
        '08:00-09:00': 12,
        '09:00-12:00': 7,
        '12:00-19:00': 7,
        '19:00-20:00': 9
    },
    "tuesday": {
        '04:00-08:00': 8,
        '08:00-11:00': 8,
        '11:00-16:00': 7,
        '16:00-17:00': 8,
        '17:00-19:00': 7,
        '19:00-20:00': 7,
    },
    "wednesday": {
        '04:00-05:00': 13,
        '05:00-06:00': 12,
        '06:00-07:00': 13,
        '07:00-08:00': 13,
        '08:00-12:00': 7,
        '12:00-13:00': 7,
        '13:00-15:00': 7,
        '15:00-18:00': 8,
        '18:00-19:00': 7,
        '19:00-20:00': 7
    },
    "thursday": {
        '06:00-07:00': 10,
        '07:00-11:00': 9,
        '11:00-12:00': 12,
        '12:00-16:00': 8,
        '16:00-17:00': 9,
        '17:00-18:00': 7,
        '18:00-19:00': 7,
        '19:00-20:00': 7
    },
    "friday": {

        '00:00-05:00': 3,
        '05:00-06:00': 10,
        '06:00-07:00': 10,
        '07:00-08:00': 12,
        '08:00-11:00': 8,
        '11:00-12:00': 7,
        '13:00-19:00': 9,
        '19:00-23:00': 3,
        '23:00-23:59': 3
    },
    "saturday": {
        '00:00-01:00': 7,
        '01:00-02:00': 10,
        '02:00-03:00': 10,
        '03:00-04:00': 11,
        '04:00-05:00': 10,
        '05:00-07:00': 10,
        '07:00-09:00': 10,
        '09:00-18:00': 10,
        '18:00-19:00': 10,
        '19:00-20:00': 10,
        '20:00-22:00': 11,
        '22:00-23:59': 10,
    },
    "sunday": {
        '00:00-04:00': 10,
        '04:00-05:00': 10,
        '05:00-09:00': 10,
        '09:00-10:00': 10,
        '10:00-11:00': 10,
        '11:00-17:00': 10,
        '17:00-18:00': 17,
        '18:00-19:00': 17,
        '19:00-20:00': 17,
    }
}



test = 0


