from datetime import datetime

import mysql.connector
import ujson
import ujson as json
from mysql.connector import Error


# Database connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host='diidrbs.mysql.polardb.rds.aliyuncs.com',
        port=3306,
        user='administrator',
        password='!admin123',
        database='diidrbs',
    )
    return connection


# Check if the email exists
def check_email_exists(email):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT email FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None


# Get user data by email
def get_user_data_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT email, name, permission FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return {'email': result[0], 'name': result[1], 'permission': result[2]}
    return None


# Get all room data
def get_all_room_data_for_user(permission):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM room"
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

            # Filter based on permission
            if permission == "Student" and access != 0:
                continue
            elif permission == "Staff" and access not in [0, 1]:
                continue
            # selected staff can access all rooms, no filter needed

            room_data = {
                "id": room_id,
                "name": room_name,
                "access": access,
                "capacity": capacity,
                "equipment": equipment,
                "location": location,
                "info": info if info else ""
            }

            booking_records = ujson.loads(get_booking_record_of_a_room(room_id))
            room_data["booking"] = booking_records

            class_data = ujson.loads(get_class_of_a_room(room_id))
            room_data["class"] = class_data

            rooms.append(room_data)

        return rooms

    return None


# Get booking records of a room and return as JSON
def get_booking_record_of_a_room(room_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM booking WHERE room_id = %s"
        cursor.execute(query, (room_id,))
        results = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    booking_records = []

    for row in results:
        time_str = row[4]
        time_points = time_str.split(",")
        time_array = [int(point) for point in time_points]

        booking_record = {
            "booking_id": row[0],
            "user_email": row[1],
            "room_id": row[2],
            "date": row[3],
            "time": time_array,
            "purpose": row[5],
            "status": row[6],
        }
        booking_records.append(booking_record)

    return ujson.dumps(booking_records, default=str)


# Get class of a room
def get_class_of_a_room(room_id):
    return ujson.dumps([], default=str)


# Get detailed room data
def get_room_detailed(room_id):
    primission = "any"
    all_rooms = get_all_room_data_for_user(primission)

    # Find the room with the given room_id
    this_room = None
    for room in all_rooms:
        if room['id'] == room_id:
            this_room = room
            break

    if this_room:
        this_room["booking"] = ujson.loads(get_booking_record_of_a_room(this_room["id"]))
        this_room["class"] = ujson.loads(get_class_of_a_room(this_room["id"]))
        print(this_room)
        return this_room

    return None


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
    time = booking_data["time"]
    purpose = booking_data["purpose"]
    status = booking_data["status"]

    query = """
    UPDATE booking
    SET room_id = %s,
        date = %s,
        time = %s,
        purpose = %s,
        status = %s
    WHERE booking_id = %s
    """
    cursor.execute(query, (room_id, date, time, purpose, status, booking_id))
    connection.commit()

    cursor.close()
    connection.close()


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


if __name__ == '__main__':
    get_room_detailed(1)
    fetch_bookings()

    modify_booking({
        "booking_id": "1710976683000",
        "date": "Fri, 15 Feb 2025 00:00:00 GMT",
        "purpose": "test11111",
        "room_id": 15,
        "status": "Confirmed",
        "time": "10",
        "user_email": "2542999@dundee.ac.uk"
    })
