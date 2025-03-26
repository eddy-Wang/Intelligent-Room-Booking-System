from datetime import datetime
from .models import get_db_connection


def update_booking_status_to_missed():
    """Update bookings' status to 'Missed' and check blacklist"""
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        today_date = datetime.today().strftime('%Y-%m-%d')

        select_query = """
            SELECT DISTINCT user_email
            FROM booking
            WHERE status = 'Confirmed' AND date <= %s
        """
        cursor.execute(select_query, (today_date,))
        users_to_check = cursor.fetchall()

        update_query = """
            UPDATE booking
            SET status = 'Missed'
            WHERE status = 'Confirmed' AND date <= %s
        """
        cursor.execute(update_query, (today_date,))
        connection.commit()

        for (user_email,) in users_to_check:
            blacklist_check_and_set(user_email)

        print(f"Booking status updated to 'Missed' for bookings on or before {today_date}.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()


def blacklist_check_and_set(user_email):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
                SELECT COUNT(*) as cnt
                FROM booking
                WHERE status = 'Missed'
                  AND user_email = %s
                  AND STR_TO_DATE(date, %s) >= DATE_SUB(NOW(), INTERVAL 30 DAY);
            """
    cursor.execute(query, (user_email, '%Y-%m-%d',))
    missed_count = cursor.fetchone()[0]

    if missed_count >= 3:
        cursor.execute("""
                        INSERT INTO user_blacklist (user_email, missed_time)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE added_at = NOW(), missed_time = %s;
                    """, (user_email, missed_count, missed_count))
        connection.commit()
        print(f"User {user_email} has been added to the blacklist due to {missed_count} missed appointments")
        return True
    else:
        print(f"User {user_email} currently has {missed_count} missed appointments (below threshold)")
        return False



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
