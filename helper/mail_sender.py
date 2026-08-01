import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

    
def send_mail(user_email, otp):
    sender_mail = os.getenv("EMAIL")
    send_pass = os.getenv("APP_PASSWORD")
    print(sender_mail, send_pass)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
   
    message = EmailMessage()
    message["subject"] = "Your Token!"
    message["from"] = sender_mail
    message["to"] = user_email
    message.set_content(f"""
                    Your OTP is: {otp}
                    Copy this code to verify your account.
                    """)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_mail, send_pass)
            server.send_message(message)
            return {"success":True,"message":"Email Sent Successfully"}
    except Exception as e:
        return {"error": e}

# send_mail()