from flask import Blueprint, request, jsonify, session
from ..models import db, User
import random, re, smtplib, ssl
from email.mime.text import MIMEText
auth_bp = Blueprint('auth', __name__)
import re
auth_bp.secret_key = "yoursecretkey"


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    company_name = data.get('company_name')
    email = data.get('email')
    password = data.get('password')

    if not company_name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    # Password validation checks
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long."}), 400
    if not re.search(r'[A-Z]', password):
        return jsonify({"error": "Password must include at least one uppercase letter."}), 400
    if not re.search(r'[a-z]', password):
        return jsonify({"error": "Password must include at least one lowercase letter."}), 400
    if not re.search(r'\d', password):
        return jsonify({"error": "Password must include at least one digit."}), 400
    if not re.search(r'[@$!%*?&]', password):
        return jsonify({"error": "Password must include at least one special character (@$!%*?&)."}), 400

    # Generate code and save temp data in session
    code = str(random.randint(100000, 999999))
    session['pending_user'] = {
        "company_name": company_name,
        "email": email,
        "password": password  # store plain temp, but better encrypt
    }
    session['verification_code'] = code

    # Send email with code
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = 's01410921@gmail.com'
    password_app = 'ydyt ujcd wvdf xcdt'  # Not your normal Gmail password

    message = MIMEText(f"Your registration verification code is: {code}")
    message["Subject"] = "Verify Your Email"
    message["From"] = sender_email
    message["To"] = email

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password_app)
        server.sendmail(sender_email, email, message.as_string())

    return jsonify({"message": "Verification code sent to email"}), 200

@auth_bp.route('/verify-registration', methods=['POST'])
def verify_registration():
    data = request.get_json()
    code = data.get('code')

    if not code or session.get('verification_code') != code:
        return jsonify({"error": "Invalid code"}), 400

    pending_user = session.get('pending_user')
    if not pending_user:
        return jsonify({"error": "No pending registration"}), 400

    # Create user
    user = User(
        company_name=pending_user['company_name'],
        email=pending_user['email']
    )
    user.set_password(pending_user['password'])

    db.session.add(user)
    db.session.commit()

    # clear session
    session.pop('pending_user', None)
    session.pop('verification_code', None)

    return jsonify({"message": "User registered successfully!"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    session['user_id'] = user.id
    session.permanent = True
    return jsonify({"message": "Login successful!", "company_name": user.company_name, "email": user.email}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200

@auth_bp.route('/session')
def get_session():
    return jsonify({
        "permanent": session.permanent,
        "user_id": session.get('user_id')
    })

@auth_bp.route('/logged')
def check_session():
    if 'user_id' in session:
        return jsonify({"logged_in": True, "user_id": session['user_id']}), 200
    else:
        return jsonify({"logged_in": False}), 200

