import random
import string
from flask_mail import Message
from . import mail

# stored the code
verification_codes = {}

def generate_verification_code():
    """generate a random verification code"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def send_verification_email(user_email, code):
    """send verification email"""
    msg = Message("Your Verification Code", recipients=[user_email])
    msg.body = f"Your verification code is: {code}"
    try:
        mail.send(msg)
        print("Verification email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

def remove_verification_code(user_email):
    """Remove the verification code for the given email."""
    if user_email in verification_codes:
        del verification_codes[user_email]