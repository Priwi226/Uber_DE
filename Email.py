import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import Nadstavenia

# Údaje pre pripojenie k SMTP serveru Wedos
SMTP_SERVER = Nadstavenia.SMTP
SMTP_PORT = 587  # Port pre STARTTLS
SMTP_USERNAME = Nadstavenia.Email_meno
SMTP_PASSWORD = Nadstavenia.Email_heslo

# Údaje pre odoslanie emailu
SENDER_EMAIL = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
RECIPIENT_EMAILS = ['xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']
EMAIL_SUBJECT = 'Auftragsinformation - xxxxxxxxxxxxxxxxxxxx'
# EMAIL_BODY = 'Toto je telo emailu.'

def send_email(EMAIL_BODY):
    # Vytvorenie multipart správy
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(RECIPIENT_EMAILS)
    msg['Subject'] = EMAIL_SUBJECT

    # Pridanie textu emailu
    msg.attach(MIMEText(EMAIL_BODY, "html"))

    # Vytvorenie SMTP spojenia s podporou STARTTLS
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()

    # Autentifikácia na SMTP serveri
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    # Odoslanie emailu
    server.send_message(msg)
    server.quit()

# Odoslanie emailu na viac adresátov
#send_email(EMAIL_BODY)

# Spustenie funkcie na odoslanie emailu
#send_email()
