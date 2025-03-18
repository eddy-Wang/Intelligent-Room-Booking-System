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
def fetch_rooms_id_and_name():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT room_id, name FROM room where deleted = 0"
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

def add_room(room_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    room_name = room_data["name"]
    capacity = room_data["capacity"]
    location = room_data["location"]
    equipment = ",".join(room_data["equipment"]) if isinstance(room_data["equipment"], list) else room_data["equipment"]
    access = room_data["access"]
    information = room_data["information"]

    try:
        check_query = "SELECT room_id FROM room WHERE name = %s"
        cursor.execute(check_query, (room_name,))
        existing_room = cursor.fetchone()

        if existing_room:
            return False, 'Room with this name already exists!'

        insert_query = """
               INSERT INTO room (name, capacity, location, equipment, access, info, deleted)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
           """
        cursor.execute(insert_query, (room_name, capacity, location, equipment, access, information, 0))
        connection.commit()

        return True, 'Room added successfully!'
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()

def modify_room(room_id, room_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    room_name = room_data["name"]
    capacity = room_data["capacity"]
    location = room_data["location"]
    equipment = ",".join(room_data["equipment"]) if isinstance(room_data["equipment"], list) else room_data["equipment"]
    access = room_data["access"]
    information = room_data["information"]
    try:
        check_query = "SELECT room_id FROM room WHERE name = %s AND room_id != %s"
        cursor.execute(check_query, (room_name, room_id))
        existing_room = cursor.fetchone()

        if existing_room:
            return False, 'Another room with this name already exists!'

        update_query = """
                UPDATE room SET name=%s, capacity=%s, location=%s, equipment=%s, access=%s, info=%s
                WHERE room_id = %s
            """
        cursor.execute(update_query, (room_name, capacity, location, equipment, access, information, room_id))
        connection.commit()

        return True, 'Room modified successfully!'
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()


def delete_room(room_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE room SET deleted = 1 WHERE room_id = %s"

    try:
        cursor.execute(query, (room_id,))
        connection.commit()
        return True, 'Room deleted successfully!'
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()


def fetch_room():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM room where deleted = 0"
        cursor.execute(query)
        result = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    if result:
        rooms = []

        for row in result:
            room_id = row[0]
            room_name = str(row[1])
            access = row[2]
            capacity = row[3]
            equipment = str(row[4])
            location = row[5]
            info = row[6]

            room_data = {
                "id": room_id,
                "name": room_name,
                "access": access,
                "capacity": capacity,
                "equipment": equipment,
                "location": location,
                "info": info if info else ""
            }

            rooms.append(room_data)

        return True, rooms
    return False, None

# Get all room issue reports
def get_all_room_issue_reports():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM room_issue_report"
        cursor.execute(query)
        result = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    reports = []
    for row in result:
        report = {
            "timestamp": row[0],
            "room_id": row[1],
            "user_email": row[2],
            "reportInfo": row[3],
            "reviewed": row[4],
        }
        reports.append(report)

    return reports

# Create a new room issue report
def create_room_issue_report(timestamp, room_id, user_email, reportInfo, reviewed="Unreviewed"):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO room_issue_report (timestamp, room_id, user_email, reportInfo, reviewed)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (timestamp, room_id, user_email, reportInfo, reviewed))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error creating report: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

# Update a room issue report
def update_room_issue_report(timestamp, reviewed=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "UPDATE room_issue_report SET "
        updates = []
        params = []

        if reviewed is not None:
            updates.append("reviewed = %s")
            params.append(reviewed)

        query += ", ".join(updates) + " WHERE report_id = %s"
        params.append(timestamp)

        cursor.execute(query, tuple(params))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error updating report: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

# Delete a room issue report
def delete_room_issue_report(timestamp):
    connection = get_db_connection()
    cursor = connection.cursor()
    report_id = timestamp

    try:
        query = "DELETE FROM room_issue_report WHERE report_id = %s"
        cursor.execute(query, (report_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error deleting report: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()








