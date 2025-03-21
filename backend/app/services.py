import random
import string
from flask_mail import Message
from mysql.connector import Error
import socket
from dateutil import parser

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


def sending_booking_email(user_email, room_id, date, time, status, purpose):
    """send booking email based on status"""
    subject = "Room Booking Status"

    if user_email is None or room_id is None or purpose is None:
        print(user_email, room_id, purpose)
        raise ValueError("Error: Missing essential booking details.")

    room_name = fetch_name_by_id(room_id)

    time_mapping = {
        0: '08:00-08:45', 1: '08:55-09:40', 2: '10:00-10:45', 3: '10:55-11:40',
        4: '12:00-12:45', 5: '12:55-13:40', 6: '14:00-14:45', 7: '14:55-15:40',
        8: '16:00-16:45', 9: '16:55-17:40', 10: '19:00-19:45', 11: '19:55-20:40'
    }

    if time is None:
        raise ValueError("Error: Received 'None' for time.")

    time = list(map(int, time.split(','))) if isinstance(time, str) else time
    sorted_times = sorted(time)
    time_slots = [time_mapping[time_idx] for time_idx in sorted_times]
    formatted_time = ', '.join(time_slots)

    if date is None:
        raise ValueError("Error: Received 'None' for date.")

    if not isinstance(date, str):
        date = str(date)

    try:
        date_obj = parser.parse(date)
        formatted_date = date_obj.strftime('%Y-%m-%d')
    except ValueError:
        formatted_date = date

    if status == "Confirmed":
        body = f"""
        Dear User,

        Your room booking has been successfully confirmed.

        Booking Details:
        Room: {room_name}
        Date: {formatted_date}
        Time: {formatted_time}
        Purpose: {purpose}

        Thank you for using booking service.

        Best regards,
        DIICSU Room Booking Service
        """
    elif status == "Pending":
        body = f"""
        Dear User,

        We have received your room booking request, and it is currently pending approval.

        Booking Details:
        Room ID: {room_name}
        Date: {formatted_date}
        Time: {formatted_time}
        Purpose: {purpose}

        Please wait for the administrator's approval.

        Best regards,
        DIICSU Room Booking Service
        """
    elif status == "Declined":
        body = f"""
        Dear User,

        Sorry, the administrator has cancelled your booking.

        Booking Details:
        Room ID: {room_name}
        Date: {formatted_date}
        Time: {formatted_time}
        Purpose: {purpose}

        If you have any question, please send an email to administrator.

        Best regards,
        DIICSU Room Booking Service
        """
    elif status == "Modify":
        body = f"""
        Dear User,

        Administrator has changed your booking details as following. Please check your new booking details.

        Booking Details:
        Room ID: {room_name}
        Date: {formatted_date}
        Time: {formatted_time}
        Purpose: {purpose}

        If you have any question, please send an email to administrator.

        Best regards,
        DIICSU Room Booking Service
            """
    elif status == "CancelByUser":
        body = f"""
        Dear User,
        
        Your room booking of {room_name} on {formatted_date} during {formatted_time} has been cancelled.
        
        Thank you for using booking service.
        
        Best regards,
        DIICSU Room Booking Service

"""
    else:
        body = f"""
        Dear User,
        
        There is an error happened with your booking request.
        
        Please contact support for assistance.

        Best regards,
        DIICSU Room Booking Service
        
        """

    msg = Message(subject, recipients=[user_email])
    msg.body = body

    try:
        mail.send(msg)
        print("Booking email sent successfully.")
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


def fetch_name_by_id(room_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT name FROM room where room_id = %s"
    cursor.execute(query, (room_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result is not None:
        return result[0]


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
    WHERE room_id = %s AND date = %s AND status = 'Confirmed'
    """

    cursor.execute(query_check, (room_id, date))
    existing_bookings = cursor.fetchall()

    time_slots_set = set(time_slots)

    for existing_time in existing_bookings:
        existing_time_slots_set = set(existing_time[0].split(","))
        if time_slots_set & existing_time_slots_set:

            print(f"Room is already booked during the time slots {existing_time_slots_set}.")
            cursor.close()
            connection.close()
            return False, "The room is already booked at the specified time."

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
    return True, "Booking successfully modified."


def add_room(room_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    room_name = room_data["name"]
    capacity = room_data["capacity"]
    location = room_data["location"]
    equipment = ",".join(room_data["equipment"]) if isinstance(room_data["equipment"], list) else room_data["equipment"]
    access = room_data["access"]
    information = room_data["information"]
    image_url = room_data["image_url"]

    try:
        check_query = "SELECT room_id FROM room WHERE name = %s"
        cursor.execute(check_query, (room_name,))
        existing_room = cursor.fetchone()

        if existing_room:
            return False, 'Room with this name already exists!'

        insert_query = """
               INSERT INTO room (name, capacity, location, equipment, access, info, deleted, image_url)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
           """
        cursor.execute(insert_query, (room_name, capacity, location, equipment, access, information, 0, image_url))
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
    image_url = room_data["image_url"]

    try:
        check_query = "SELECT room_id FROM room WHERE name = %s AND room_id != %s"
        cursor.execute(check_query, (room_name, room_id))
        existing_room = cursor.fetchone()

        if existing_room:
            return False, 'Another room with this name already exists!'

        update_query = """
                UPDATE room SET name=%s, capacity=%s, location=%s, equipment=%s, access=%s, info=%s, image_url=%s
                WHERE room_id = %s
            """
        cursor.execute(update_query,
                       (room_name, capacity, location, equipment, access, information, image_url, room_id))
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
            image_url = row[7]
            deleted = row[8]

            if deleted:
                continue

            room_data = {
                "id": room_id,
                "name": room_name,
                "access": access,
                "capacity": capacity,
                "equipment": equipment,
                "location": location,
                "info": info if info else "",
                "image_url": image_url if image_url else "",
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
            INSERT INTO room_issue_report (report_id, room_id, user_email, reportInfo, reviewed)
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
