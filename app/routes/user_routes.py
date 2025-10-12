from flask import Blueprint, jsonify, session, current_app, render_template
from ..models import db, User, UserCustomer
from .reminder import send_weekly_reminders
from sqlalchemy import inspect

user_bp = Blueprint('users', __name__)

@user_bp.route('/')
def home():
    return render_template('index.html')

@user_bp.route('/ping', methods=['GET'])
def ping():
    current_app.logger.info("Ping success")
    return jsonify({"message": "Ping success"}), 200

@user_bp.route('/remind', methods=['GET'])
def remind_test():
    send_weekly_reminders(current_app._get_current_object())
    return jsonify({"message": "Reminders sent"})

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "company_name": u.company_name, "email": u.email}
        for u in users
    ])

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@user_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    
    return jsonify({"company_name": user.company_name, "email": user.email}), 200

@user_bp.route('/user-customer', methods=['GET'])
def user_customers():
    users = User.query.all()
    result = []

    for user in users:
        # For each user, get all their associated customers
        customers_list = [
            {
                "customer_id": uc.customer.id,
                "email": uc.customer.email,
                "points": uc.points,
                "last_reminder_sent": uc.last_reminder_sent.isoformat() if uc.last_reminder_sent else None
            }
            for uc in user.customers
        ]
        result.append({
            "user_id": user.id,
            "company_name": user.company_name,
            "email": user.email,
            "customers": customers_list
        })

    return jsonify(result), 200

