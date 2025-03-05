# 业务逻辑

import random
from flask_mail import Message
from . import mail

verification_codes = {}


def generate_verification_code():
    return str(random.randint(100000, 999999))


def send_verification_email(user_email, code):
    msg = Message("Your Verification Code", recipients=[user_email])
    msg.body = f"Your verification code is: {code}"
    try:
        mail.send(msg)
        print("Verification email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)
