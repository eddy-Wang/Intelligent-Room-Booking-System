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

# Fetch users from the database
def fetch_users():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    # Format the result into a list of dictionaries for each user
    users = []
    for row in result:
        user_data = {
            "email": row[0],
            "name": row[1],
            "permission": row[2]
        }
        users.append(user_data)

    return users


# Fetch rooms from the database
def fetch_rooms():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT room_id, name FROM room"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    # Format the result into a list of dictionaries for each room
    rooms = []
    for row in result:
        room_data = {
            "room_id": row[0],
            "name": row[1]
        }
        rooms.append(room_data)

    return rooms


# Fetch all bookings from the database
def fetch_bookings():
    # Fetch all bookings from the database
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM booking"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    bookings = []
    for row in result:
        booking_data = {
            "booking_id": row[0],
            "user_email": row[1],
            "room_id": row[2],
            "date": row[3],
            "time": row[4],
            "purpose": row[5],
            "status": row[6]
        }
        bookings.append(booking_data)
    print(bookings)
    return bookings


# Update booking status
def update_booking_status(booking_id, status):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE booking SET status = %s WHERE booking_id = %s"
    cursor.execute(query, (status, booking_id))
    connection.commit()
    cursor.close()
    connection.close()


# Delete a booking
def delete_booking(booking_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM booking WHERE booking_id = %s"
    cursor.execute(query, (booking_id,))
    connection.commit()
    cursor.close()
    connection.close()


def modify_booking(booking_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    booking_id = booking_data["booking_id"]
    room_id = booking_data["room_id"]
    date = booking_data["date"]
    time_slots = booking_data["time"]
    purpose = booking_data["purpose"]
    status = booking_data["status"]

    query_check = """
    SELECT time
    FROM booking
    WHERE room_id = %s AND date = %s AND booking_id != %s
    """

    cursor.execute(query_check, (room_id, date, booking_id))
    existing_bookings = cursor.fetchall()

    time_slots_set = set(time_slots)

    for existing_time in existing_bookings:
        existing_time_slots_set = set(map(int, existing_time[0].split(',')))
        if time_slots_set & existing_time_slots_set:
            print(f"Room {room_id} is already booked during the time slots {existing_time_slots_set}.")
            cursor.close()
            connection.close()
            return "The room is already booked at the specified time."

    query_update = """
    UPDATE booking
    SET room_id = %s,
        date = %s,
        time = %s,
        purpose = %s,
        status = %s
    WHERE booking_id = %s
    """

    cursor.execute(query_update, (room_id, date, ','.join(map(str, time_slots_set)), purpose, status, booking_id))
    connection.commit()

    cursor.close()
    connection.close()
    return "Booking successfully modified."