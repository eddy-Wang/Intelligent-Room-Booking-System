import os
import time

from flask import Blueprint, request, jsonify, session
from .services import generate_verification_code, send_verification_email, verification_codes, remove_verification_code, \
    get_user_reservations, cancel_reservation, fetch_users, fetch_rooms_id_and_name, fetch_bookings, \
    update_booking_status, \
    delete_booking, modify_booking, add_room, modify_room, delete_room, fetch_room, update_room_issue_report, \
    create_room_issue_report, delete_room_issue_report, get_all_room_issue_reports, sending_booking_email, \
    send_conflict_email, send_ban_email, booking_check_in_service, generate_ics_content
from .models import check_email_exists, get_user_data_by_email, get_room_detailed, \
    get_all_room_data_for_user, add_room_issue, set_room_issue_reviewed, set_room_issue_report_info, get_booking_by_id, \
    get_bad_user_list, reset_missed_times_for_user, get_db_connection, get_permission_by_email
from .utils import is_user_blacklisted

# Set the blueprint
bp = Blueprint('routes', __name__)


def create_response(code, message, data=None):
    """Helper function to create a consistent response format."""
    return jsonify({
        'code': code,
        'message': message,
        'data': data if data is not None else {}
    })

@bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """
    Login
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    user_email = data.get('email')

    if not user_email:
        return create_response('001', 'Email is required!')

    if not check_email_exists(user_email):
        return create_response('002', 'Email does not exist!')

    code = generate_verification_code()
    print(code)
    send_verification_email(user_email, code)
    verification_codes[user_email] = {'code': code, 'timestamp': time.time()}  # Store code and timestamp

    return create_response('000', 'Verification code sent!')


@bp.route('/verify-code', methods=['POST', 'OPTIONS'])
def verify_code():
    """
    Verify the code for login
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    user_email = data.get('email')
    entered_code = data.get('code')

    if not user_email or not entered_code:
        return create_response('003', 'Email and code are required!')

    # Check if the verification code is expired (60 seconds limit)
    if user_email in verification_codes:
        code_data = verification_codes[user_email]
        current_time = time.time()
        # If the code is older than 60 seconds, it expires
        if current_time - code_data['timestamp'] > 60:
            remove_verification_code(user_email)  # Remove expired code
            return create_response('006', 'Verification code has expired! Please request a new code.')

        # If the entered code matches
        if code_data['code'] == entered_code:
            # After verification, fetch user details and return them
            user_data = get_user_data_by_email(user_email)
            if user_data:
                remove_verification_code(user_email)
                session['user_data'] = user_data
                return create_response('000', 'Login successful!', user_data)
            else:
                return create_response('005', 'Failed to retrieve user data.')
        else:
            return create_response('004', 'Invalid code, please try again.')
    else:
        return create_response('007', 'No verification code sent. Please request a new code.')


@bp.route('/me', methods=['GET', 'OPTIONS'])
def me():
    """
    Verify the user by seesion
    :return: message
    """
    if 'user_data' not in session:
        return 'Unauthorized', 401
    else:
        return create_response('000', "", session.get('user_data'))


@bp.route('/allRoom', methods=['GET', 'OPTIONS'])
def allRoom():
    """
    Get the data of all rooms
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    permission = session.get('user_data').get('permission')
    print(permission)
    if not permission:
        return create_response('003', 'Permission parameter is required!')

    all_room_data = get_all_room_data_for_user(permission)
    if all_room_data:
        return create_response('001', 'All Rooms found!', all_room_data)
    else:
        return create_response('002', 'No Rooms found!')


@bp.route('/requestRoomDetails', methods=['GET', 'OPTIONS'])
def requestRoomDetails():
    """
    Get all data of the room (by ID)
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    room_id = request.args.get('roomId')

    room_data = get_room_detailed(room_id)
    if room_data:
        return create_response('001', 'Room found!', room_data)
    else:
        return create_response('002', 'Room not found!')


@bp.route('/get-reservations', methods=['POST', 'OPTIONS'])
def get_reservations():
    """
    Get the data of all reservations
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    user_email = data.get('email')

    if not user_email:
        return create_response('001', 'Email is required!')

    reservations = get_user_reservations(user_email)
    return create_response('000', 'Reservations retrieved successfully!', reservations)


@bp.route('/cancel-reservation', methods=['POST', 'OPTIONS'])
def cancel_reservation_route():
    """
    Cancel reservation with booking_id
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    booking_id = data.get('booking_id')
    print(booking_id)

    if not booking_id:
        return create_response('001', 'Booking ID is required!')

    if cancel_reservation(booking_id):
        this_booking = get_booking_by_id(booking_id)
        user_email = this_booking.get('user_email')
        room_id = this_booking.get('room_id')
        date = this_booking.get('date')
        booking_time = this_booking.get('time')
        purpose = this_booking.get('purpose')

        sending_booking_email(user_email, room_id, date, booking_time, 'CancelByUser', purpose)
        return create_response('000', 'Reservation cancelled successfully!')
    else:
        return create_response('002', 'Failed to cancel reservation. It may already be processed or does not exist.')



@bp.route('/users', methods=['GET'])
def get_users():
    """
    Fetch the data of all users
    :return: message
    """
    try:
        users = fetch_users()
        return create_response('000', 'Users fetched successfully!', users)
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')



@bp.route('/rooms_id_and_name', methods=['GET'])
def get_rooms_id_and_name():
    """
    Fetch the id and name of all rooms
    :return: message
    """
    try:
        rooms = fetch_rooms_id_and_name()
        print(rooms)
        return create_response('000', 'Rooms fetched successfully!', rooms)
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')



@bp.route('/bookings', methods=['GET'])
def get_bookings():
    try:
        bookings = fetch_bookings()
        print(bookings)
        return create_response('000', 'Bookings fetched successfully!', bookings)
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


# Update booking status route
@bp.route('/bookings/<int:id>', methods=['PUT'])
def update_booking(id):
    """
    Update the data of one booking
    :param id:
    :return: message
    """
    data=request.json
    status = data.get('status')

    message=''
    if data.get('cancel_reason') is not None:
        print("cancel reason")

        message = data.get('cancel_reason')
        print(message)
    if not status:
        return create_response('400', 'Status is required.')

    try:
        update_booking_status(id, status)
        this_booking = get_booking_by_id(id)
        user_email = this_booking.get('user_email')
        room_id = this_booking.get('room_id')
        date = this_booking.get('date')
        time = this_booking.get('time')
        purpose = this_booking.get('purpose')

        sending_booking_email(user_email, room_id, date, time, status, purpose, message)
        return create_response('000', 'Booking updated successfully!')
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')



@bp.route('/bookings/<int:id>', methods=['DELETE'])
def delete_booking_route(id):
    """
    Delete the data of one booking
    :param id:
    :return: message
    """
    try:
        delete_booking(id)
        return create_response('000', 'Booking deleted successfully!')
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


@bp.route('/modifyBooking', methods=['PUT', 'OPTIONS'])
def modify_booking_route():
    """
    Modify the data of one booking
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200
    booking_data = request.get_json()
    try:
        success, message =modify_booking(booking_data)
        if success:
            room_id = booking_data.get('room_id')
            date = booking_data.get('date')
            time_slots = booking_data.get('time')
            purpose = booking_data.get('purpose')
            user_email = booking_data.get('user_email', 'test@example.com')
            time_str = ",".join(map(str, time_slots))
            sending_booking_email(user_email, room_id, date, time_str, 'Modify',purpose)
            return create_response('001', message)
        else:
            return create_response('002', message)
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


@bp.route('/bookRoom', methods=['POST', 'OPTIONS'])
def book_room():
    """
    Book a room
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    user_email = data.get('user_email', 'test@example.com')
    if is_user_blacklisted(user_email):
        return create_response('007', 'you are in the blacklist')

    required_fields = ['roomId', 'date', 'timeSlots', 'purpose']
    for field in required_fields:
        if field not in data or not data[field]:
            return create_response('003', f'{field} is required.')

    room_id = data.get('roomId')
    room_name = data.get('roomName', '')
    date = data.get('date')
    time_slots = data.get('timeSlots')
    purpose = data.get('purpose')
    user_email = data.get('user_email', 'test@example.com')

    try:
        # Check if the time is OK
        from .models import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()

        query_check = "SELECT time FROM booking WHERE room_id = %s AND date = %s AND status IN ('Confirmed','Banned')"
        cursor.execute(query_check, (room_id, date))
        existing_bookings = cursor.fetchall()

        requested_slots_set = set(time_slots)
        for (existing_time_str,) in existing_bookings:
            if existing_time_str.strip():
                existing_slots = set(map(int, existing_time_str.split(',')))
            else:
                existing_slots = set()
            if requested_slots_set.intersection(existing_slots):
                cursor.close()
                conn.close()
                return create_response('005', 'Room already booked for one or more selected time slots.')

        query_access = "SELECT access FROM room WHERE room_id = %s"
        cursor.execute(query_access, (room_id,))
        result = cursor.fetchone()
        if result:
            room_access = result[0]
        else:
            cursor.close()
            conn.close()
            return create_response('006', 'Room not found.')

        permission = get_permission_by_email(user_email)
        print(permission)
        status = "Confirmed" if room_access == 0 or permission == "Admin" else "Pending"
        print(status)
        time_str = ",".join(map(str, time_slots))
        booking_id = str(int(time.time() * 1000))

        query = """
            INSERT INTO booking (booking_id, user_email, room_id, date, time, purpose, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (booking_id, user_email, room_id, date, time_str, purpose, status))
        conn.commit()
        cursor.close()
        conn.close()
        sending_booking_email(user_email, room_id, date, time_str, status, purpose)
        return create_response('000', 'Booking successful!')
    except Exception as e:
        return create_response('004', f'Booking failed: {str(e)}')


@bp.route('/getRooms', methods=['GET', 'OPTIONS'])
def rooms():
    """
    Fetch rooms
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    success, data = fetch_room()

    if success:
        return create_response('000', "All room fetched!", data)
    else:
        return create_response('001', "No room fetched!", data)


@bp.route('/rooms', methods=['POST', 'OPTIONS'])
def addRooms():
    """
    Add a room
    :return:
    """
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    required_fields = ['name', 'capacity', 'location', 'equipment', 'access', 'information', 'image_url']

    for field in required_fields:
        if field not in data:
            return create_response('001', f'{field} is required!')

    success, message = add_room(data)

    if success:
        return create_response('000', message)
    else:
        return create_response('002', message)

@bp.route('/subscribe_calendar/<string:email>', methods=['GET'])
def subscribe_calendar(email):
    """
    Subscribe to calendar
    :param email:
    :return: the ics file
    """
    try:
        ics_content = generate_ics_content(email)
        print(1)
        print(ics_content)

        ics_file_path = os.path.join('static', f'{email}.ics')
        os.makedirs(os.path.dirname(ics_file_path), exist_ok=True)
        with open(ics_file_path, 'w') as file:
            file.write(ics_content)

        return ics_content
    except Exception as e:
        return str(e), 500

@bp.route('/download_calendar/<string:email>', methods=['GET'])
def download_calendar(email):
    """
    Download calendar
    :param email:
    :return: the ics file
    """
    try:
        ics_content = generate_ics_content(email)
        return ics_content
    except Exception as e:
        print(f"Error downloading calendar: {e}")
        return str(e), 500

@bp.route('/ban', methods=['POST', 'OPTIONS'])
def set_ban_period():
    """
    Ban the room for a period of time
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    required_fields = ['room_id', 'date', 'time']
    for field in required_fields:
        if field not in data or not data[field]:
            return create_response('400', f'Missing required fields: {field}')

    room_id = data['room_id']
    date = data['date']
    time_slots = list(map(int, data['time']))
    print(time_slots)
    time_str = ','.join(map(str, sorted(set(time_slots))))
    print(time_str)
    purpose = data['purpose'] if 'purpose' in data else 'Banned from administrator'
    user_email = data['user_email']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT booking_id FROM booking 
            WHERE room_id=%s 
              AND date=%s 
              AND time=%s 
              AND status='Banned'
        """, (room_id, date, time_str))
        if cursor.fetchone():
            return create_response('409', 'This prohibited time period already exists')

        booking_id = str(int(time.time() * 1000))
        cursor.execute("""
            INSERT INTO booking 
            (booking_id, user_email, room_id, date, time, purpose, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Banned')
        """, (booking_id, user_email, room_id, date, time_str, purpose))

        cursor.execute("""
            SELECT booking_id, user_email, time 
            FROM booking 
            WHERE room_id=%s 
              AND date=%s 
              AND status IN ('Pending','Confirmed')
        """, (room_id, date))

        # Cancel all related booking
        conflict_count = 0
        for (bid, email, exist_time) in cursor.fetchall():
            exist_slots = set(map(int, exist_time.split(',')))
            if exist_slots & set(time_slots):
                cursor.execute("""
                    UPDATE booking 
                    SET status='Declined' 
                    WHERE booking_id=%s
                """, (bid,))
                conflict_count += 1

                send_conflict_email(email, room_id, date, exist_time, purpose)


        conn.commit()

        send_ban_email(user_email, room_id, date, time_str, purpose)

        return create_response('200', 'Prohibited time period set successfully', {
            'conflict_count': conflict_count,
            'ban_id': booking_id
        })


    except Exception as e:
        conn.rollback()
        return create_response('500', f'server error: {str(e)}')
    finally:
        cursor.close()
        conn.close()

@bp.route('/rooms/<int:room_id>', methods=['PUT'])
def modify_room_route(room_id):
    """
    Modify room details
    :param room_id:
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    required_fields = ['name', 'capacity', 'location', 'equipment', 'access', 'information', 'image_url']
    for field in required_fields:
        if field not in data:
            return create_response('001', f'{field} is required!')

    success, message = modify_room(room_id, data)

    if success:
        return create_response('000', message)
    else:
        return create_response('002', message)


@bp.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room_route(room_id):
    """
    Delete room (soft way)
    :param room_id:
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    success, message = delete_room(room_id)
    if success:
        return create_response('000', message)
    else:
        return create_response('002', message)


@bp.route('/room_issue', methods=['PUT'])
def put_room_issue():
    """
    Report the issue.
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    required_fields = ['room_id', 'user_email', 'report_info', 'user_permission']

    for field in required_fields:
        if field not in data:
            return create_response('001', f'{field} is required!')

    success, message = add_room_issue(data['room_id'], data['user_email'], data['report_info'], data['user_permission'])

    if success:
        return create_response('000', message)
    else:
        return create_response('002', message)


@bp.route('/room_issue/status', methods=['POST'])
def modify_room_issue_status():
    """
    Modify the room issue status
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    required_fields = ['report_id', 'value']

    for field in required_fields:
        if field not in data:
            return create_response('001', f'{field} is required!')

    success, message = set_room_issue_reviewed(data['report_id'], data['value'])

    if success:
        return create_response('000', message)
    else:
        return create_response('002', message)


@bp.route('/room_issue/report_info', methods=['POST'])
def modify_room_issue_report_info():
    """
    Modify the room issue report info
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    required_fields = ['report_id', 'value']

    for field in required_fields:
        if field not in data:
            return create_response('001', f'{field} is required!')

    success, message = set_room_issue_report_info(data['report_id'], data['value'])

    if success:
        return create_response('000', message)
    else:
        return create_response('002', message)


@bp.route('/room_issue_reports', methods=['GET'])
def get_reports():
    """
    Get all room issue reports
    :return: message
    """
    try:
        reports = get_all_room_issue_reports()
        return create_response('000', 'Reports fetched successfully!', reports)
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


@bp.route('/room_issue_reports', methods=['POST'])
def create_report():
    """Create new issue report for admin"""
    data = request.json
    try:
        timestamp = str(int(time.time() * 1000))
        room_id = data['room_id']
        user_email = data['user_email']
        reportInfo = data['reportInfo']
        reviewed = data.get('reviewed', 'Unreviewed')

        if create_room_issue_report(timestamp, room_id, user_email, reportInfo, reviewed):
            return create_response('000', 'Report created successfully!')
        else:
            return create_response('400', 'Failed to create report.')
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


@bp.route('/room_issue_reports/<string:report_id>', methods=['PUT'])
def update_report(report_id):
    """
    Update room issue report
    :param report_id:
    :return: message
    """
    data = request.json
    try:
        if update_room_issue_report(
                report_id,
                reviewed=data.get('reviewed'),
        ):
            return create_response('000', 'Report updated successfully!')
        else:
            return create_response('400', 'Failed to update report.')
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


@bp.route('/room_issue_reports/<string:timestamp>', methods=['DELETE'])
def delete_report(timestamp):
    """
    Delete room issue report
    :param timestamp:
    :return: message
    """
    try:
        if delete_room_issue_report(timestamp):
            return create_response('000', 'Report deleted successfully!')
        else:
            return create_response('400', 'Failed to delete report.')
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')

@bp.route('/bad_users', methods=['GET'])
def get_bad_users():
    """
    Get all blacklisted users
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    resBool, resData = get_bad_user_list()

    if resBool:
        return create_response('000',"Get bad users successfully!",resData)
    else:
        return create_response('500',"Error: "+resData)

@bp.route('/reset_missed_times/<string:user_email>', methods=['GET'])
def reset_missed_times(user_email):
    """
    Reset missed times of a user
    :param user_email:
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    resBool, resData = reset_missed_times_for_user(user_email)

    if resBool:
        return create_response('000',resData)
    else:
        return create_response('500',"Error: "+resData)

@bp.route('/booking_check_in/<string:booking_id>', methods=['GET'])
def booking_check_in(booking_id):
    """
    Check in
    :param booking_id:
    :return: message
    """
    if request.method == 'OPTIONS':
        return '', 200

    resBool, resData = booking_check_in_service(booking_id)

    if resBool:
        return create_response('000', resData)
    else:
        return create_response('500', "Error: " + resData)
