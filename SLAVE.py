import ftplib
from datetime import datetime, timedelta
import os
import Nadstavenia
import time
import traceback
from selenium import webdriver
import traceback
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.options import Options
from UberLogin import Uber_login
from Telo import Telo
import spravy
import Nadstavenia
import FTP
import threading
import time
import sys
import signal


# Funkcia pre načítanie dátumu a času zo súboru na FTP serveri
def get_file_datetime(ftp, filepath):
    directory, filename = os.path.split(filepath)
    ftp.cwd(directory)  # Nastaví aktuálny pracovný adresár na zodpovedajúci adresár na FTP serveri
    ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)
    with open(filename, 'r') as file:
        data = file.read().strip()
        file_datetime = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
    return file_datetime


def Slave(telegram_mess, chrome_driver):
    # Pripojenie na FTP server
    ftp = ftplib.FTP(Nadstavenia.FTP_NAME)
    ftp.login(Nadstavenia.FTP_MENO, Nadstavenia.FTP_HESLO)

    file_directory = Nadstavenia.FTP_Cesta
    file_name = Nadstavenia.FTP_SUBOR

    file_path = os.path.join(file_directory, file_name)

    last_file_datetime = None  # Inicializácia premennej pre posledný nájdený súbor
    reset_inner_loop = True  # Premenná pre sledovanie stavu vnorenej slučky

    while True:
        # Získanie aktuálneho dátumu a času
        current_datetime = datetime.now()

        # Získanie dátumu a času zo súboru na FTP serveri
        file_datetime = get_file_datetime(ftp, file_path)

        if last_file_datetime is not None:
            # Výpočet časového rozdielu medzi posledným nájdeným súborom a aktuálnym časom
            time_difference = current_datetime - last_file_datetime
            time_difference_seconds = int(time_difference.total_seconds())

            if time_difference_seconds < Nadstavenia.FTP_cas:
                # Ak je časový rozdiel menší ako hodnota FTP_cas, čakajte
                print(f"Čakanie... Časový rozdiel: {time_difference_seconds} sekúnd")
                time.sleep(5)  # Pauza 5 sekúnd
                continue  # Preskočenie ďalšieho vykonávania kódu

        # Aktualizácia hodnoty pre posledný nájdený súbor
        last_file_datetime = file_datetime

        # Vaša ďalšia logika a akcie
        # Tu pridajte váš ďalší kód, ktorý chcete vykonať pri prekročení časového limitu

        if last_file_datetime is not None:
            # Výpočet časového rozdielu v sekundách
            time_difference_seconds = int((current_datetime - last_file_datetime).total_seconds())

            if time_difference_seconds >= Nadstavenia.FTP_cas:
                while True:
                    try:
                        if Nadstavenia.Prehliadac_on == 1:
                            driver = webdriver.Chrome(chrome_driver)
                        elif Nadstavenia.Prehliadac_on != 1:
                            options = Options()
                            options.add_argument("--headless")  # Nastavenie pre bezhlavý režim
                            driver = webdriver.Chrome(chrome_driver, options=options)

                        if Nadstavenia.test == 1:
                            driver = webdriver.Chrome('/home/zakazky/chromedriver')  # Zmente cestu k chromedriveru podľa vašej inštalácie

                            # Načítanie stránky zo súboru
                            file_path = '/home/priwi/Pytho_projekty/Uber klicker/Testovanie/stranka/stranka.html'  # Upravte cestu k uloženému súboru
                            driver.get('file://' + file_path)

                        else:
                            # Otvorenie webstránky
                            driver.get("https://vsdispatch.uber.com/?_csid=PI2_JgqPI4yzCRC-fkUx-Q&state=ZfeVISTBMotT-qmcRViboIsoH3nACIoKh7KW4sxbbkw%3D&wstate=AjC600RsKE0gpR-FKiw8Gp9bKGQ64gwFZ8LG6CLqYXM%3D&effect=")

                        Uber_login(driver)
                        Posledna_zakazka = None
                        Adresa_vyzdvyhnutia = None
                        Adresa_vylozenia = None
                        old_tab = None

                        Telo(driver, Posledna_zakazka, Adresa_vyzdvyhnutia, Adresa_vylozenia, old_tab)

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
                        spravy.me_send_to_telegram(telegram_mess + "\n\n" + error_message_with_code)
                        spravy.send_to_telegram(telegram_mess + "\n\n" + error_message_with_code)

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
                        break

        # Koniec vášho ďalšieho kódu

        time.sleep(5)  # Počkajte 5 sekúnd pred ďalším cyklom

    # Ukončenie pripojenia na FTP server
    ftp.quit()
