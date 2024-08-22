#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 20:50:38 2021
"""

import traceback
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.options import Options
from UberLogin import Uber_login
from Telo import Telo
from spravy import me_send_to_telegram
from spravy import send_to_telegram
import Nadstavenia
import FTP
import threading
import time
import os


telegram_mess = "RUF GLEICH ZUM CHEF. Auftrags system ist runtergefalen !!!!!! UBER" + Nadstavenia.STROJ

user_name = os.getlogin()
os.system (f"rm -rf /home/{user_name}/.cache/google-chrome/*")
os.system (f"rm -rf /home/{user_name}/.cache/selenium/*")
os.system (f"rm -rf __pycache__")


chrome_driver = f"/home/{user_name}/chromedriver"
# chrome_driver =()

try:
    if Nadstavenia.Prehliadac_on == 1:
        driver = webdriver.Chrome(chrome_driver)
    elif Nadstavenia.Prehliadac_on != 1:
        options = Options()
        options.add_argument("--headless")  # Nastavenie pre bezhlavý režim
        driver = webdriver.Chrome(chrome_driver, options=options)

    # Otvorenie webstránky
    driver.get("https://auth.uber.com/v2/?breeze_init_req_id=0af7bc82-2fa0-4e5f-84bb-8dd7ccec0599&breeze_local_zone=dca24&next_url=https%3A%2F%2Fsupplier.uber.com%2F&state=_Qt5o7k2YfcgMJiDec-NW91jTzrbHs0kE3W8YUW9Srk%3D")
    # driver.get("https://vsdispatch.uber.com/?_csid=PI2_JgqPI4yzCRC-fkUx-Q&state=ZfeVISTBMotT-qmcRViboIsoH3nACIoKh7KW4sxbbkw%3D&wstate=AjC600RsKE0gpR-FKiw8Gp9bKGQ64gwFZ8LG6CLqYXM%3D&effect=")

    Uber_login(driver)
    Posledna_zakazka = None
    Adresa_vyzdvyhnutia = None
    Adresa_vylozenia = None
    old_tab = None

    if Nadstavenia.STROJ == "Master":
        def run_ftp_write():
            while True:
                FTP.FTP_write()
                time.sleep(60)

        thread = threading.Thread(target=run_ftp_write)
        thread.daemon = True  # Nastavenie vlákna ako démonského
        thread.start()
    
    driver.get("https://vsdispatch.uber.com/?_csid=PI2_JgqPI4yzCRC-fkUx-Q&state=ZfeVISTBMotT-qmcRViboIsoH3nACIoKh7KW4sxbbkw%3D&wstate=AjC600RsKE0gpR-FKiw8Gp9bKGQ64gwFZ8LG6CLqYXM%3D&effect=")
    Telo(driver, Posledna_zakazka, Adresa_vyzdvyhnutia, Adresa_vylozenia, old_tab)
    driver.quit()

except Exception as e:
    # Ak nastane zlyhanie, zaznamenajte chybovú správu
    error_message = str(e)
    
    # Získanie posledných dvoch riadkov kódu
    code_lines = traceback.format_exc().strip().split('\n')
    last_two_lines = code_lines[-3:]
    code_snippet = "\n".join(last_two_lines)
    error_message_with_code = f"{code_snippet}\n\n{error_message}"
    driver.quit()
    
    # Odoslanie Telegram správy s chybovou hláškou a výpisom kódu
    me_send_to_telegram(telegram_mess + "\n\n" + error_message_with_code)
    send_to_telegram(telegram_mess + "\n\n" + error_message_with_code)
    print(telegram_mess + "\n\n" + error_message_with_code)
    
    # Získanie informácií o problematickom prvku
    element_info = ""
    if isinstance(e, selenium.common.exceptions.StaleElementReferenceException):
        element = driver.find_element_by_id("id_prvku")  # Nahraďte "id_prvku" skutočným identifikátorom prvku
        element_info = f"Prvok: {element.tag_name} s id={element.get_attribute('id')} a class={element.get_attribute('class')}"
        print("Informácie o problematickom prvku:")
        print(element_info)

    # Zápis do súboru Log.txt
    log_message = f"{telegram_mess}\n\n{error_message_with_code}\n\n{element_info}"
    with open("Log.txt", "w") as file:
        file.write(log_message)
    driver.quit()

# Zápis do súboru Log.txt
with open("Log.txt", "w") as file:
    file.write(telegram_mess + "\n\n" + error_message_with_code + "\n")
