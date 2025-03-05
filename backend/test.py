import random
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'rf_diicsu_rb@163.com'
app.config['MAIL_PASSWORD'] = 'VAY5wcSNdMhDkZQv'
app.config['MAIL_DEFAULT_SENDER'] = 'rf_diicsu_rb@163.com'

mail = Mail(app)
CORS(app)

verification_codes = {}

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(user_email, code):
    msg = Message("Your Verification Code", recipients=[user_email])
    msg.body = f"Your verification code is: {code}"
    try:
        mail.send(msg)
        print("Verification email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

@app.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    data = request.get_json()
    user_email = data['email']
    code = generate_verification_code()
    send_verification_email(user_email, code)
    verification_codes[user_email] = code
    print(f"Stored codes: {verification_codes}")
    return jsonify({'message': 'Verification code sent!'})

@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    user_email = data['email']
    entered_code = data['code']
    if verification_codes.get(user_email) == entered_code:
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid code, please try again.'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
