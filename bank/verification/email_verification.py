import smtplib
from email.message import EmailMessage
import os

def send_email_gmail(to_email, password, name, fname):
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_app_pass = os.environ.get("GMAIL_APP_PASS")

    if not gmail_user or not gmail_app_pass:
        raise RuntimeError("Set GMAIL_USER and GMAIL_APP_PASS environment variables.")


    
    msg = EmailMessage()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = '🚨 Security alert: password request'
    msg.set_content(f"""Hello {name} {fname},\n\n
This message is from Vault-Tech Bank Security Team.\n
As requested, here is your account password:
>>>        {password}       <<<

If you did not request this, please ignore this email. For your security, we recommend changing your password immediately and contacting Vault-Tech Bank Support.\n

Stay safe,
Vault-Tech Bank — Security Team 🔐
""")
    with open("bank/verification/logo.jpg", "rb") as f:
        logo = f.read()
    msg.add_attachment(logo, maintype="image", subtype="jpeg", filename="logo.jpg")



    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(gmail_user, gmail_app_pass)
        s.send_message(msg)
