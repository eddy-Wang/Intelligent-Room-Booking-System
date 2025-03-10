import mysql.connector
import json
# from .config import Config

def get_db_connection():
    connection = mysql.connector.connect(
        # host=Config.DB_HOST,
        # port=Config.DB_PORT,
        # user=Config.DB_USER,
        # password=Config.DB_PASSWORD,
        # database=Config.DB_NAME,
        host='diidrbs.mysql.polardb.rds.aliyuncs.com',
        port = 3306,
        user = 'administrator',
        password = '!admin123',
        database = 'diidrbs',
    )
    return connection

def check_email_exists(email):
    """check if the email exists"""
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT email FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None

def get_user_data_by_email(email):
    """get user data by email"""
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

def get_all_room_data():
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
        rooms = {}

        for row in result:
            room_id = row[0]
            room_name = str(row[1])
            access = row[2]
            capacity = row[3]
            equipment = str(row[4])
            location = row[5]
            info = row[6]

            room_data = {
                "room_id": room_id,
                "name": room_name,
                "access": access,
                "capacity": capacity,
                "equipment": equipment,
                "location": location,
                "info": info if info else ""
            }

            booking_records = json.loads(get_booking_record_of_a_room(room_id))
            room_data["booking"] = booking_records

            class_data = json.loads(get_class_of_a_room(room_id))
            room_data["class"] = class_data

            rooms[room_id] = room_data

        print(json.dumps(rooms))
        return json.dumps(rooms, indent=4, ensure_ascii=False)

    return None

def get_booking_record_of_a_room(room_id):
    """Get booking records of a room and return as JSON"""
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM booking WHERE room_id = %s"
        cursor.execute(query, (room_id,))

        # Fetch all results before closing cursor
        results = cursor.fetchall()

    finally:
        cursor.close()  # Now safe to close since all results are fetched
        connection.close()

    booking_records = []

    for row in results:
        booking_record = {
            "booking_id": row[0],
            "user_email": row[1],
            "room_id": row[2],
            "date": row[3],
            "time": row[4],
            "purpose": row[5],
            "status": row[6],
        }
        booking_records.append(booking_record)

    return json.dumps(booking_records, default=str)

def get_class_of_a_room(room_id):
    return json.dumps([], default=str)

def get_room_detailed(room_id):
    all_rooms = json.loads(get_all_room_data())
    this_room = all_rooms.get(str(room_id), None)

    if this_room:
        this_room["booking"] = json.loads(get_booking_record_of_a_room(this_room["room_id"]))
        this_room["class"] = json.loads(get_class_of_a_room(this_room["room_id"]))
        print(json.dumps(this_room, default=str))
        return json.dumps(this_room, default=str)

    return None

if __name__ == '__main__':
    get_all_room_data()
    get_room_detailed(1)

