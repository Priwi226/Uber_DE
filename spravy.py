import requests
import threading
import time
import Nadstavenia 

def send_to_telegram(message):
    apiToken = Nadstavenia.Telegram_api_Token_uber
    chatID = Nadstavenia.Telegram_miestnost_uber
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        formatted_message = """
        <b>Toto je tučný text</b>
        <i>Toto je text kurzívou</i>
        <code>Toto je blokový kód</code>
        <b><font color="red">Toto je červený text</font></b>
        <b><font color="green">Toto je zelený text</font></b>
        """
        
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message, 'parse_mode': 'HTML'})
        print(response.text)
        
        delay = int(Nadstavenia.Telegram_mazanie)
        delete_message(chatID, response.json()['result']['message_id'], delay)
    except Exception as e:
        print(e)



def send_to_telegram_with_timer(message):
    thread = threading.Thread(target=send_to_telegram, args=(message,))
    thread.start()
    

def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    
    apiToken = Nadstavenia.Telegram_api_Token_uber
    apiURL = f'https://api.telegram.org/bot{apiToken}/deleteMessage'
    
    try:
        response = requests.post(apiURL, json={'chat_id': chat_id, 'message_id': message_id})
        print(response.text)
    except Exception as e:
        print(e)
        

def kiwi_send_to_telegram(message):
    apiToken = Nadstavenia.Telegram_api_Token_kiwi
    chatID = Nadstavenia.Telegram_miestnost_kiwi
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        formatted_message = """
        <b>Toto je tučný text</b>
        <i>Toto je text kurzívou</i>
        <code>Toto je blokový kód</code>
        <b><font color="red">Toto je červený text</font></b>
        <b><font color="green">Toto je zelený text</font></b>
        """
        
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message, 'parse_mode': 'HTML'})
        print(response.text)
    except Exception as e:
        print(e)


def me_send_to_telegram(message):
    apiToken = Nadstavenia.Telegram_api_Token_uber
    chatID = Nadstavenia.Telegram_miestnost_ja
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        formatted_message = """
        <b>Toto je tučný text</b>
        <i>Toto je text kurzívou</i>
        <code>Toto je blokový kód</code>
        <b><font color="red">Toto je červený text</font></b>
        <b><font color="green">Toto je zelený text</font></b>
        """
        
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message, 'parse_mode': 'HTML'})
        print(response.text)
    except Exception as e:
        print(e)
