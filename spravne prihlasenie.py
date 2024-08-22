# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:54:48 2023

@author: Premium Limo Service
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

import Nadstavenia




######  Telegram nadstavenia
def send_to_telegram(message):

    apiToken = (Nadstavenia.Telegram_api_Token)
    chatID = (Nadstavenia.Telegram_miestnost)
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
  #  STROJF = ("<font color=\"#FF0000\"> " + (Nadstavenia.STROJ) + ("<font color=\"#FF0000\">"))

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

#   Urcenie prehliadaca selenium 
driver = webdriver.Chrome('c:/chromedriver.exe')

#   Otvorenie webowej stranky
# driver.get("https://vsdispatch.uber.com/?_csid=QdK9AVCblxReIE56NhNu5w&effect=&state=ZfeVISTBMotT-qmcRViboIsoH3nACIoKh7KW4sxbbkw%3D&wstate=Ej3LoDGIMpb04N3WrLHH-y6aS5TI_yTa0RiWyNqSSYU%3D")
driver.get("https://auth.uber.com/v2/?breeze_init_req_id=0af7bc82-2fa0-4e5f-84bb-8dd7ccec0599&breeze_local_zone=dca24&next_url=https%3A%2F%2Fsupplier.uber.com%2F&state=_Qt5o7k2YfcgMJiDec-NW91jTzrbHs0kE3W8YUW9Srk%3D")

print(driver.title)
time.sleep (3)
################################################


############################################################Najdenie pola Prihlasovanie email
try:
    prihlasenie_email = driver.find_element("id", "PHONE_NUMBER_or_EMAIL_ADDRESS" )
    # Ak sa element1 nájde, vykonaj niektorý kód tu
    prihlasenie_email.send_keys(Nadstavenia.MENO)
    prihlasenie_email.send_keys(Keys.RETURN)
    time.sleep(5)
except NoSuchElementException:
    # Ak sa element1 nenájde, vykonaj niektorý kód tu
    print("prihlasovaci email nenajdeny")
    send_to_telegram("Prihlasovaci email NENAJDENY " + (Nadstavenia.STROJ) +"")
    

    
############################################################Najdenie pola prishlasenie starym heslom 
try:
   prihlasnie_SMS = driver.find_element(By.ID, "alt-PASSWORD")
   print("Detekovanie stareho hesla hesla")
   prihlasnie_SMS.click()
   time.sleep (5)
except NoSuchElementException:
    # Ak sa element1 nenájde, vykonaj niektorý kód tu
    print("Tlacidlo stary email nenajdeny")
    send_to_telegram("Tlacidlo stary email NENAJDENY " + (Nadstavenia.STROJ) +"")
    
    
    
    
############################################################Najdenie SMS pola
try:  
    PIN = driver.find_element("id", "PHONE_SMS_OTP-0")
    send_to_telegram("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
    print("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
    SMS_CODE = input("Aky je SMS/WhatsApp Kluc?")
except NoSuchElementException:
    # Ak sa element1 nenájde, vykonaj niektorý kód tu
    print("SMS pole nenajdene")
    
try:
    PIN = driver.find_element("id", "PHONE_SMS_OTP-0")
    PIN.send_keys(SMS_CODE)
    time.sleep(5)
except NoSuchElementException:
    print ("Nenajdene pole SMS")
    
try:
    PIN_whatsup = driver.find_element(By.ID, "PHONE_WHATSAPP_OTP-0")
    PIN_whatsup.send_keys(SMS_CODE)
    time.sleep(5)
except NoSuchElementException:
    print("Nenajdene pole wahtsup")


#############################################################Najdenie pola heslo
try:
    prihlasenie_heslo = driver.find_element(By.ID, "PASSWORD" )
    prihlasenie_heslo.send_keys(Nadstavenia.HESLO)
    prihlasenie_heslo.send_keys(Keys.RETURN)

except NoSuchElementException:
    # Ak sa element1 nenájde, vykonaj niektorý kód tu
    print("SMS NENAJDENY")
    

##############################################################
time.sleep(5)
print("Prihlasenie OK")
send_to_telegram("Prihlasenie \n" + (Nadstavenia.STROJ) + "\nOK")

    
    
    
    
    
    
