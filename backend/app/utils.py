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

