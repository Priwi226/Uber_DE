#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 20:57:46 2023

@author: priwi
"""

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import Telegram
import Nadstavenia


def Uber_login(driver):
    try:
        prihlasenie_email = driver.find_element("id", "PHONE_NUMBER_or_EMAIL_ADDRESS" )
        # Ak sa element1 nájde, vykonaj niektorý kód tu
        prihlasenie_email.send_keys(Nadstavenia.MENO)
        prihlasenie_email.send_keys(Keys.RETURN)
        time.sleep(5)
    except NoSuchElementException:
        # Ak sa element1 nenájde, vykonaj niektorý kód tu
        print("prihlasovaci email nenajdeny")
        Telegram.kiwi_send_to_telegram("Prihlasovaci email NENAJDENY " + (Nadstavenia.STROJ) +"")
    

    
############################################################Najdenie pola prishlasenie starym heslom 
    try:
        prihlasnie_SMS = driver.find_element(By.ID, "alt-PASSWORD")
        print("Detekovanie stareho hesla hesla")
        prihlasnie_SMS.click()
        time.sleep (5)
    except NoSuchElementException:
        # Ak sa element1 nenájde, vykonaj niektorý kód tu
        print("Tlacidlo stary email nenajdeny")
        Telegram.kiwi_send_to_telegram("Tlacidlo stary email NENAJDENY " + (Nadstavenia.STROJ) +"")
    
    
    
    
############################################################Najdenie SMS pola
    try:  
        PIN = driver.find_element("id", "PHONE_SMS_OTP-0")
        Telegram.kiwi_send_to_telegram("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
        print("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
        time.sleep(2)
        SMS_CODE = input("Aky je SMS/WhatsApp Kluc?")
    except NoSuchElementException:
        # Ak sa element1 nenájde, vykonaj niektorý kód tu
        print("SMS pole nenajdene")
    
    try:  
        PIN = driver.find_element("id", "PHONE_WHATSAPP_OTP-0")
        Telegram.kiwi_send_to_telegram("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
        print("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
        time.sleep(2)
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
    Telegram.kiwi_send_to_telegram("Prihlasenie \n" + (Nadstavenia.STROJ) + "\nOK")