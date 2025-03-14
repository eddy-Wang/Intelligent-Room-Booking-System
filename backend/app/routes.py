import time
from flask import Blueprint, request, jsonify
from .services import generate_verification_code, send_verification_email, verification_codes, remove_verification_code, \
    get_user_reservations, cancel_reservation, fetch_users, fetch_rooms, fetch_bookings, update_booking_status, \
    delete_booking, modify_booking
from .models import check_email_exists, get_user_data_by_email, get_room_detailed, \
    get_all_room_data_for_user

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
@bp.route('/rooms', methods=['GET'])
def get_rooms():
    try:
        rooms = fetch_rooms()
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
    print(request.json)
    status = request.json.get('status')
    if not status:
        return create_response('400', 'Status is required.')

    try:
        update_booking_status(id, status)
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

@bp.route('/modifyBooking', methods=['PUT','OPTIONS'])
def modify_booking_route():
    if request.method == 'OPTIONS':
        return '', 200
    booking_data = request.get_json()
    try:
        modify_booking(booking_data)
        return create_response('000', 'Booking updated successfully!')
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

        query_check = "SELECT time FROM booking WHERE room_id = %s AND date = %s"
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
        return create_response('000', 'Booking successful!')
    except Exception as e:
        return create_response('004', f'Booking failed: {str(e)}')