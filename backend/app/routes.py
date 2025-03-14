import time
from flask import Blueprint, request, jsonify
from .services import generate_verification_code, send_verification_email, verification_codes, remove_verification_code, \
    get_user_reservations, cancel_reservation, fetch_users, fetch_bookings, fetch_rooms, update_booking_status, \
    modify_booking, delete_booking
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

