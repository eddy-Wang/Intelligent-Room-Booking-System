import random
import string
from flask_mail import Message
from mysql.connector import Error
import socket

socket.getfqdn = lambda name=None: "localhost"

from . import mail
from .models import get_db_connection

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


# Get user reservations by email
def get_user_reservations(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT b.booking_id, b.date, b.time, b.purpose, b.status, r.name, r.capacity
    FROM booking b
    JOIN room r ON b.room_id = r.room_id
    WHERE b.user_email = %s
    ORDER BY b.date, b.time
    """
    cursor.execute(query, (email,))
    reservations = cursor.fetchall()
    cursor.close()
    connection.close()
    return reservations


# Cancel reservation by booking ID
def cancel_reservation(booking_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE booking SET status = 'Declined' WHERE booking_id = %s AND status = 'Confirmed'"
    try:
        cursor.execute(query, (booking_id,))
        connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Error as e:
        print(f"Error cancelling reservation: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
