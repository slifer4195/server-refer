from flask import Blueprint, jsonify, request, session
import smtplib
from email.message import EmailMessage
from ..models import db, Customer, MenuItem, UserCustomer


point_bp = Blueprint('points', __name__)

def send_email(to_email, subject, body):
    sender_email = 's01410921@gmail.com'
    app_password = 'tdyt ujcd wvdf xcdt'  # Not your normal Gmail password

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        return {"success": True}
    except Exception as e:
        return {"success": False}

def increase_point_internal(user_id, customer_id, change=1):
    assoc = (
        db.session.query(UserCustomer)
        .filter_by(user_id=user_id, customer_id=customer_id)
        .first()
    )

    if not assoc:
        return jsonify({'error': 'Customer not found for this user'}), 404

    assoc.points = max(0, min(100, assoc.points + int(change)))
    db.session.commit()

    return jsonify({
        'success': True,
        'points': assoc.points
    })

@point_bp.route('/send-test-email', methods=['POST'])
def send_test_email():
    data = request.get_json()
    recipient = data.get('to')
    subject = data.get('subject', 'Hello from Flask')
    body = data.get('body', 'This is a test email.')

    user_id = data.get('user_id')
    customer_id = data.get('customer_id')
    point = int(data.get('point', 1))

    if not recipient or not user_id or not customer_id:
        return jsonify({'error': 'Missing required fields'}), 400

    # Send the email
    mail_result = send_email(recipient, subject, body)

    if not mail_result["success"]:
        return jsonify({
            'error': 'Failed to send email',
            'message': mail_result["message"]
        }), 500

    # Only increase points if email succeeded
    assoc = (
        db.session.query(UserCustomer)
        .filter_by(user_id=user_id, customer_id=customer_id)
        .first()
    )

    if not assoc:
        return jsonify({'error': 'Customer not found for this user'}), 404

    if point > 0:
        assoc.points = max(0, min(100, assoc.points + point))
        db.session.commit()

    return jsonify({
        'success': True,
        'customer_id': assoc.customer_id,
        'email': assoc.customer.email,
        'points': assoc.points,
        'message': f"Email sent to {recipient} and {point} points added"
    }), 200


@point_bp.route('/customer_point/<int:customer_id>', methods=['GET'])
def get_customer_points(customer_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Find the association record for this user + customer
    assoc = (
        db.session.query(UserCustomer)
        .join(Customer)
        .filter(
            UserCustomer.customer_id == customer_id,
            UserCustomer.user_id == user_id
        )
        .first()
    )

    if not assoc:
        return jsonify({'error': 'Customer not found for this user'}), 404

    return jsonify({
        'customer_id': assoc.customer.id,
        'email': assoc.customer.email,
        'points': assoc.points
    }), 200


@point_bp.route('/deduct_point/<int:customer_id>/<int:item_id>', methods=['GET'])
def deduct_point(customer_id, item_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Find association row (customer <-> user)
    assoc = (
        db.session.query(UserCustomer)
        .join(Customer)
        .filter(
            UserCustomer.customer_id == customer_id,
            UserCustomer.user_id == user_id
        )
        .first()
    )

    if not assoc:
        return jsonify({'error': 'Customer not found for this user'}), 404

    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    required_points = item.required_points

    if assoc.points < required_points:
        return jsonify({'error': 'Not enough points'}), 400

    # Deduct points
    assoc.points -= required_points
    db.session.commit()

    # Prepare email content
    subject = f"Points Deducted for {item.name}"
    body = (
        f"Hello {assoc.customer.email},\n\n"
        f"{required_points} points have been deducted for redeeming '{item.name}'.\n"
        f"Your current point balance is: {assoc.points}.\n\n"
        f"Thank you!"
    )

    # Send the email
    mail_result = send_email(assoc.customer.email, subject, body)
    if not mail_result["success"]:
        return jsonify({
            'customer_id': assoc.customer.id,
            'email': assoc.customer.email,
            'points': assoc.points,
            'message': f'Points deducted but failed to send email: {mail_result["message"]}'
        }), 500

    return jsonify({
        'customer_id': assoc.customer.id,
        'email': assoc.customer.email,
        'points': assoc.points,
        'message': f'Deducted {required_points} points for item {item.name}, email sent successfully.'
    }), 200

