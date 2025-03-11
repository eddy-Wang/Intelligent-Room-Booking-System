import mysql.connector
from .config import Config

def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
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
from mysql.connector import Error

def get_user_reservations(email):
    """Get all reservations for a user by email."""
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

def cancel_reservation(booking_id):
    """Cancel a reservation by setting its status to 'Cancelled'."""
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE booking SET status = 'Cancelled' WHERE booking_id = %s AND status = 'Pending'"
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