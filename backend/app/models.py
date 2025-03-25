from datetime import datetime

import mysql.connector
import ujson
from .config import Config
from mysql.connector import Error


# Database connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,

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
        booking_dict = get_all_booking_records()

        lesson_dict = get_all_lessons()

        report_dict = get_all_report()

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
                "info": info if info else "",
                "image_url": image_url if image_url else ""
            }

            room_data["booking"] = booking_dict.get(room_id, [])
            room_data["lesson"] = lesson_dict.get(room_id, [])
            room_data["report"] = report_dict.get(room_id, [])

            rooms.append(room_data)

        return rooms

    return None

def get_all_booking_records():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM booking WHERE status = 'Confirmed'"
        cursor.execute(query)
        results = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    booking_dict = {}

    for row in results:
        room_id = row[2]
        time_str = row[4]
        time_points = time_str.split(",")
        time_array = [int(point) for point in time_points if point.strip()]

        booking_record = {
            "booking_id": row[0],
            "user_email": row[1],
            "room_id": room_id,
            "date": row[3],
            "time": time_array,
            "purpose": row[5],
            "status": row[6],
        }

        if room_id not in booking_dict:
            booking_dict[room_id] = []
        booking_dict[room_id].append(booking_record)

    return booking_dict


def get_all_lessons():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM lesson"
        cursor.execute(query)
        results = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    lesson_dict = {}

    for row in results:
        room_id_for_lesson = row[1]
        time_str_for_lesson = row[3]
        time_points_for_lesson = time_str_for_lesson.split(",")
        print(time_points_for_lesson)
        time_array_for_lesson = [int(point) for point in time_points_for_lesson if point.strip()]
        print(time_array_for_lesson)
        lesson_record = {
            "lesson_id": row[0],
            "room_id": room_id_for_lesson,
            "time": time_array_for_lesson,
            "date": row[2],
        }
        if room_id_for_lesson not in lesson_dict:
            lesson_dict[room_id_for_lesson] = []
        lesson_dict[room_id_for_lesson].append(lesson_record)

    return lesson_dict


def get_all_report():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT room_id, reportInfo FROM room_issue_report WHERE reviewed = 'Approved'"
        cursor.execute(query)
        results = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    report_dict = {}

    for row in results:
        room_id = row[0]
        report_info = str(row[1])

        if room_id not in report_dict:
            report_dict[room_id] = []

        report_dict[room_id].append(report_info)

    return report_dict

def get_booking_by_id(booking_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM booking WHERE booking_id = %s"
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()

    finally:
        cursor.close()
        connection.close()

    booking = {}
    if result:
        booking_id = result[0]
        user_email = result[1]
        room_id = result[2]
        date = result[3]
        time = result[4]
        purpose = result[5]
        status = result[6]

        booking = {
            "booking_id": booking_id,
            "user_email": user_email,
            "room_id": room_id,
            "date": date,
            "time": time,
            "purpose": purpose,
            "status": status,

        }
    return booking

# Get lesson of a room
def get_lesson_of_a_room(room_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM lesson WHERE room_id = %s"
        cursor.execute(query, (room_id,))
        results = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    class_records = []

    for row in results:
        lesson_id = row[0]
        room_id = row[1]
        date = row[2]
        time_str = row[3]
        time_points = time_str.split(",")
        time_array = [int(point) for point in time_points if point.strip()]

        lesson_record = {
            "lesson_id": lesson_id,
            "room_id": room_id,
            "date": date,
            "time": time_array,
        }

        class_records.append(lesson_record)

    return ujson.dumps(class_records, default=str)


def get_room_report(room_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT reportInfo FROM room_issue_report WHERE room_id = %s AND reviewed = 'Approved'"
        cursor.execute(query, (room_id,))

        results = cursor.fetchall()
        report = [str(row[0]) for row in results]

    except Exception as e:
        print(f"Error fetching room report: {e}")
        report = []

    finally:
        cursor.close()
        connection.close()

    return ujson.dumps(report, default=str)


# Get booking details of a room
def get_room_detailed(room_id):
    this_room = {"booking": ujson.loads(get_booking_record_of_a_room(room_id)),
                 "lesson": ujson.loads(get_lesson_of_a_room(room_id)),
                 "report": ujson.loads(get_room_report(room_id)),}

    print(this_room)
    return this_room


# Get booking records of a room and return as JSON
def get_booking_record_of_a_room(room_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM booking WHERE room_id = %s AND status ='Confirmed'"
        cursor.execute(query, (room_id,))
        results = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    booking_records = []

    for row in results:
        time_str = row[4]
        time_points = time_str.split(",")
        time_array = [int(point) for point in time_points if point.strip()]

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


def add_room_issue(room_id, user_email, report_info, user_permission):
    if not report_info or report_info == "":
        return False, "Empty report info."

    report_id = int(round(datetime.now().timestamp() * 1000))

    connection = get_db_connection()
    cursor = connection.cursor()
    reviewed_status = "Approved" if user_permission == "Admin" else "Unreviewed"
    try:
        query = "INSERT INTO room_issue_report (report_id, room_id, user_email, reportInfo, reviewed) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (str(report_id), room_id, user_email, report_info, reviewed_status))
        connection.commit()

        return True, "Add room issue report successfully!"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()

def set_room_issue_reviewed(report_id, value):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "UPDATE room_issue_report SET reviewed = %s WHERE report_id = %s"
        cursor.execute(query, (value, report_id))
        connection.commit()

        return True, "Set the status of issue report successfully!"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()

def set_room_issue_report_info(report_id, value):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "UPDATE room_issue_report SET reportInfo = %s WHERE report_id = %s"
        cursor.execute(query, (value, report_id))
        connection.commit()

        return True, "Set the info of issue report successfully!"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()

def get_bad_user_list():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT user_email, name, added_at, missed_time FROM user_blacklist LEFT JOIN users ON user_blacklist.user_email = users.email"
        cursor.execute(query)
        res = cursor.fetchall()
        ret = []

        for item in res:
            email = item[0]
            name = item[1]
            db_time = item[2]
            missed_time = item[3]

            result = {
                "user_email": email,
                "user_name": name,
                "added_at": db_time,
                "missed_time": missed_time
            }
            ret.append(result)

        return True, ret

    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()

def reset_missed_times_for_user(user_email):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM user_blacklist WHERE user_email = %s"
        cursor.execute(query, (user_email,))
        connection.commit()

        return True, "Reset successfully!"
    except Error as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()

def get_permission_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT permission FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        res = cursor.fetchone()

        if res:
            return res[0]
        else:
            return None

    except Exception as e:
        print("Error fetching permission:", e)
        return None

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    get_room_detailed(1)