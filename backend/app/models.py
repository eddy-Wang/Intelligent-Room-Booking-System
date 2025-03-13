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
            if permission == "student" and access != 0:
                continue
            elif permission == "staff" and access not in [0, 1]:
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

# Get booking details of a room
def get_room_detailed(room_id):
    this_room = {"booking": ujson.loads(get_booking_record_of_a_room(room_id)),
                 "class": ujson.loads(get_class_of_a_room(room_id))}

    print(this_room)
    return this_room


if __name__ == '__main__':
    get_room_detailed(1)

