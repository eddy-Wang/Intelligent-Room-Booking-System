# 定义 API 接口

from flask import Blueprint, request, jsonify
from .services import generate_verification_code, send_verification_email, verification_codes

bp = Blueprint('routes', __name__)


@bp.route('/send-verification-code', methods=['POST'])
def send_code():
    data = request.get_json()
    user_email = data.get('email')
    if not user_email:
        return jsonify({'message': 'Email is required'}), 400
    code = generate_verification_code()
    send_verification_email(user_email, code)
    verification_codes[user_email] = code
    print(f"Stored codes: {verification_codes}")
    return jsonify({'message': 'Verification code sent!'})


@bp.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    user_email = data.get('email')
    entered_code = data.get('code')
    if verification_codes.get(user_email) == entered_code:
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid code, please try again.'}), 400
