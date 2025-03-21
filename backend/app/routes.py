import time
from datetime import datetime

from flask import Blueprint, request, jsonify
from .services import generate_verification_code, send_verification_email, verification_codes, remove_verification_code, \
    get_user_reservations, cancel_reservation, fetch_users, fetch_rooms_id_and_name, fetch_bookings, \
    update_booking_status, \
    delete_booking, modify_booking, add_room, modify_room, delete_room, fetch_room, update_room_issue_report, \
    create_room_issue_report, delete_room_issue_report, get_all_room_issue_reports, sending_booking_email
from .models import check_email_exists, get_user_data_by_email, get_room_detailed, \
    get_all_room_data_for_user, add_room_issue, set_room_issue_reviewed, set_room_issue_report_info, get_booking_by_id

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
                return create_response('000', 'Login successful!', user_data)
            else:
                return create_response('005', 'Failed to retrieve user data.')
        else:
            return create_response('004', 'Invalid code, please try again.')
    else:
        return create_response('007', 'No verification code sent. Please request a new code.')


@bp.route('/allRoom', methods=['GET', 'OPTIONS'])
def allRoom():
    if request.method == 'OPTIONS':
        return '', 200

    permission = request.args.get('permission')
    if not permission:
        return create_response('003', 'Permission parameter is required!')

    all_room_data = get_all_room_data_for_user(permission)
    if all_room_data:
        return create_response('001', 'All Rooms found!', all_room_data)
    else:
        return create_response('002', 'No Rooms found!')


@bp.route('/requestRoomDetails', methods=['GET', 'OPTIONS'])
def requestRoomDetails():
    if request.method == 'OPTIONS':
        return '', 200

    room_id = request.args.get('roomId')

    room_data = get_room_detailed(room_id)
    print(room_data)
    if room_data:
        return create_response('001', 'Room found!', room_data)
    else:
        return create_response('002', 'Room not found!')


@bp.route('/get-reservations', methods=['POST', 'OPTIONS'])
def get_reservations():
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


# Fetch users route
@bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = fetch_users()
        return create_response('000', 'Users fetched successfully!', users)
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


# Fetch rooms route
@bp.route('/rooms_id_and_name', methods=['GET'])
def get_rooms_id_and_name():
    try:
        rooms = fetch_rooms_id_and_name()
        print(rooms)
        return create_response('000', 'Rooms fetched successfully!', rooms)
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


# Fetch bookings route
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
    status = request.json.get('status')
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

        sending_booking_email(user_email, room_id, date, time, status, purpose)
        return create_response('000', 'Booking updated successfully!')
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


# Delete booking route
@bp.route('/bookings/<int:id>', methods=['DELETE'])
def delete_booking_route(id):
    try:
        delete_booking(id)
        return create_response('000', 'Booking deleted successfully!')
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


@bp.route('/modifyBooking', methods=['PUT', 'OPTIONS'])
def modify_booking_route():
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
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
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
        from .models import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()

        query_check = "SELECT time FROM booking WHERE room_id = %s AND date = %s AND status = 'Confirmed'"
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

        status = "Confirmed" if room_access == 0 else "Pending"
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
    if request.method == 'OPTIONS':
        return '', 200

    success, data = fetch_room()

    if success:
        return create_response('000', "All room fetched!", data)
    else:
        return create_response('001', "No room fetched!", data)


@bp.route('/rooms', methods=['POST', 'OPTIONS'])
def getRooms():
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


@bp.route('/rooms/<int:room_id>', methods=['PUT'])
def modify_room_route(room_id):
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
    if request.method == 'OPTIONS':
        return '', 200

    success, message = delete_room(room_id)
    if success:
        return create_response('000', message)
    else:
        return create_response('002', message)


@bp.route('/room_issue', methods=['PUT'])
def put_room_issue():
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


# Get all room issue reports
@bp.route('/room_issue_reports', methods=['GET'])
def get_reports():
    try:
        reports = get_all_room_issue_reports()
        return create_response('000', 'Reports fetched successfully!', reports)
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')


# Create a new room issue report
@bp.route('/room_issue_reports', methods=['POST'])
def create_report():
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


# Update a room issue report
@bp.route('/room_issue_reports/<string:report_id>', methods=['PUT'])
def update_report(report_id):
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


# Delete a room issue report
@bp.route('/room_issue_reports/<string:timestamp>', methods=['DELETE'])
def delete_report(timestamp):
    try:
        if delete_room_issue_report(timestamp):
            return create_response('000', 'Report deleted successfully!')
        else:
            return create_response('400', 'Failed to delete report.')
    except Exception as e:
        return create_response('500', f'Error: {str(e)}')
