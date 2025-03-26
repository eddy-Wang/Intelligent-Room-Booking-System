from datetime import datetime
from .models import get_db_connection


def update_booking_status_to_missed():
    """Update bookings' status into Missed"""
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        today_date = datetime.today().strftime('%Y-%m-%d')


        update_query = """
        UPDATE booking
        SET status = 'Missed'
        WHERE status = 'Confirmed' AND date <= %s
        """
        cursor.execute(update_query, (today_date,))
        connection.commit()

        print(f"{today_date}")

    except Exception as e:
        print(f"{e}")

    finally:
        cursor.close()
        connection.close()


def is_user_blacklisted(user_email):
    """Check if user is blacklisted"""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
                    SELECT 1
                    FROM user_blacklist
                    WHERE user_email = %s
                    LIMIT 1
                """
        cursor.execute(query, (user_email,))
        return cursor.fetchone() is not None
    except Exception as e:
        return False
    finally:
        cursor.close()
        connection.close()
