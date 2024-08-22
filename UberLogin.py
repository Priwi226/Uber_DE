import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import spravy
import Nadstavenia
import sys

def Uber_login(driver):
   
    print(driver.title)




    ############################################################Najdenie pola Prihlasovanie email
    time.sleep(5)
    try:
        prihlasenie_email = driver.find_element("id", "PHONE_NUMBER_or_EMAIL_ADDRESS" )
        # Ak sa element1 nájde, vykonaj niektorý kód tu
        prihlasenie_email.send_keys(Nadstavenia.MENO)
        prihlasenie_email.send_keys(Keys.RETURN)
    
        # remaining_time = 120
        # while remaining_time > 0:
        #     sys.stdout.write(f"\rOstavajuci čas: {remaining_time} sekund")
        #     sys.stdout.flush()
        #     time.sleep(1)
        #     remaining_time -= 1
        Pokracovat = input("Potvrdenim pokracuj")
    except NoSuchElementException:
        # Ak sa element1 nenájde, vykonaj niektorý kód tu
        print("/nPrihlasovaci email nenajdeny")
    
    ###########################################################################
    time.sleep(5)
    try:
        # Najít prvek s textem "Passwort"
        password_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Passwort')or contains(text(), 'heslo')]")

        try:
            prihlasenie_heslo = driver.find_element(By.ID, "PASSWORD")
            prihlasenie_heslo.send_keys(Nadstavenia.HESLO)
            prihlasenie_heslo.send_keys(Keys.RETURN)
            print ("A")

        except NoSuchElementException:
            # Ak sa element1 nenájde, vykonaj niektorý kód tu
            print("SMS NENAJDENY")

    except NoSuchElementException:
        # Pokud prvek s textem "Passwort" neexistuje
        time.sleep(10)
        print ("B")
        volba_hesla = driver.find_element ("id", "alt-alternate-forms-option-modal")
        volba_hesla.click()
        time.sleep(10)
        email_potvrdenie = driver.find_element (By.ID, "alt-more-options-modal-password")
        email_potvrdenie.click()
        

        
    ############################################################Najdenie pola prishlasenie starym heslom 
    # Pokracovat = input("Potvrdenim pokracuj")
    # try:
    #     prihlasnie_SMS = driver.find_element(By.ID, "alt-alternate-forms-option-modal")
    #     print("Detekovanie stareho hesla hesla")
    #     prihlasnie_SMS.click()
    #     time.sleep (5)
    # except NoSuchElementException:
    #     # Ak sa element1 nenájde, vykonaj niektorý kód tu
    #     print("Tlacidlo stary email nenajdeny")
    
############################################################################################################
    time.sleep(5)
    
    try:
        # Najít prvek s textem "Passwort"
        password_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Passwort')]")
        # Pokud prvek s textem "Passwort" existuje
        try:
            prihlasenie_heslo = driver.find_element(By.ID, "PASSWORD" )
            prihlasenie_heslo.send_keys(Nadstavenia.HESLO)
            prihlasenie_heslo.send_keys(Keys.RETURN)

        except NoSuchElementException:
            # Ak sa element1 nenájde, vykonaj niektorý kód tu
            print("SMS NENAJDENY")

    except NoSuchElementException:
        # Pokud prvek s textem "Passwort" neexistuje
        print("Passwort element nenajdeny")
        try:
            volba_hesla = driver.find_element ("id", "alt-alternate-forms-option-modal")
            volba_hesla.click()
        except NoSuchElementException:
            print("Nenajdene ine volby.")
            
            
            #######################################################################
        
        
    try:
        prihlasnie_SMS = driver.find_element(By.ID, "alt-PASSWORD")
        print("Detekovanie stareho hesla hesla")
        prihlasnie_SMS.click()
        time.sleep (5)
    except NoSuchElementException:
        # Ak sa element1 nenájde, vykonaj niektorý kód tu
        print("Tlacidlo stary email nenajdeny")
        
        
        
        
        
    ############################################################Najdenie SMS pola
    try:  
        PIN = driver.find_element("id", "PHONE_SMS_OTP-0")
        spravy.me_send_to_telegram("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
        print("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
        time.sleep(2)
        SMS_CODE = input("Aky je SMS WhatsApp Kluc")
    except NoSuchElementException:
        # Ak sa element1 nenájde, vykonaj niektorý kód tu
        print("SMS pole nenajdene")
        
    try:  
        PIN = driver.find_element("id", "PHONE_WHATSAPP_OTP-0")
        spravy.me_send_to_telegram("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
        print("UBER LogIn \nVyzaduje sa SMS potvrdenie \n" + (Nadstavenia.STROJ) + "")
        time.sleep(2)
        #SMS_CODE = input("Aky je SMS/WhatsApp Kluc?")
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
    time.sleep(2)
    print("Prihlasenie OK")
    
    spravy.me_send_to_telegram("Prihlasenie \n" + (Nadstavenia.STROJ) + "\nOK")
    #####################################################