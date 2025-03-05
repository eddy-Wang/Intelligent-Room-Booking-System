import random
import string
import mysql.connector
import time
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)

# Configure mail server
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'rf_diicsu_rb@163.com'
app.config['MAIL_PASSWORD'] = 'VAY5wcSNdMhDkZQv'
app.config['MAIL_DEFAULT_SENDER'] = 'rf_diicsu_rb@163.com'

mail = Mail(app)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Database configuration
db_config = {
    'host': 'diidrbs.mysql.polardb.rds.aliyuncs.com',
    'port': 3306,
    'user': 'administrator',
    'password': '!admin123',
    'database': 'diidrbs'
}

# Dictionary to store verification codes and their timestamps
verification_codes = {}

def generate_verification_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def send_verification_email(user_email, code):
    """Send verification code email."""
    msg = Message("Your Verification Code", recipients=[user_email])
    msg.body = f"Your verification code is: {code}"
    try:
        mail.send(msg)
        print("Verification email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

def check_email_exists(email):
    """Check if the email exists in the users table."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT email FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    except mysql.connector.Error as err:
        print("Database error:", err)
        return False

def get_user_data_by_email(email):
    """Fetch user details from the database using the email."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT email, name, permission FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            # Return the user data as a dictionary
            return {'email': result[0], 'name': result[1], 'permission': result[2]}
        return None
    except mysql.connector.Error as err:
        print("Database error:", err)
        return None

def create_response(code, message, data=None):
    """Helper function to create a consistent response format."""
    return jsonify({
        'code': code,
        'message': message,
        'data': data if data is not None else {}
    })

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':  # 处理预检请求
        return '', 200

    # 处理实际的 POST 请求
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

@app.route('/verify-code', methods=['POST', 'OPTIONS'])
def verify_code():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    user_email = data.get('email')
    entered_code = data.get('code')

    if not user_email or not entered_code:
        return create_response('003', 'Email and code are required!')

    # Check if the verification code is expired (5 seconds limit)
    if user_email in verification_codes:
        code_data = verification_codes[user_email]
        current_time = time.time()
        # If the code is older than 60 seconds, it expires
        if current_time - code_data['timestamp'] > 60:
            del verification_codes[user_email]  # Remove expired code
            return create_response('006', 'Verification code has expired! Please request a new code.')

        # If the entered code matches
        if code_data['code'] == entered_code:
            # After verification, fetch user details and return them
            user_data = get_user_data_by_email(user_email)
            if user_data:
                return create_response('000', 'Login successful!', user_data)
            else:
                return create_response('005', 'Failed to retrieve user data.')
        else:
            return create_response('004', 'Invalid code, please try again.')
    else:
        return create_response('007', 'No verification code sent. Please request a new code.')

if __name__ == '__main__':
    app.run(port=8080)
