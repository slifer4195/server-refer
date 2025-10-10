from flask import Blueprint, request, jsonify, session, current_app
from ..models import db, User, Customer, UserCustomer
import re
functionality = Blueprint('functionality', __name__)

@functionality.route('/customers', methods=['GET'])
def get_customers():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Build customer list with relationship data
    customers = [
        {
            "id": uc.customer.id,
            "email": uc.customer.email,
            "points": uc.points,
            "last_reminder_sent": uc.last_reminder_sent.isoformat() if uc.last_reminder_sent else None
        }
        for uc in user.customers
    ]

    return jsonify(customers), 200


EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@functionality.route('/add-customer', methods = ["POST"])
def add_customer():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    email = data.get('email')
 
    if not email:
        return jsonify({"error": "Email is required"}), 400

    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # 1. Check if customer already exists globally
    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        # Create new customer if not in DB yet
        customer = Customer(email=email)
        db.session.add(customer)
        db.session.flush()  # make sure customer.id is available

    # 2. Check if relationship already exists for this user
    existing_link = UserCustomer.query.filter_by(user_id=user.id, customer_id=customer.id).first()
    if existing_link:
        return jsonify({"error": "Customer already linked to this business"}), 409

    # 3. Create relationship with default points = 0
    user_customer = UserCustomer(user_id=user.id, customer_id=customer.id, points=0)
    db.session.add(user_customer)
    db.session.commit()
    
    return jsonify({"success": True, "email": email}), 201

@functionality.route('/delete-customer', methods=['DELETE'])
def delete_customer():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Find the customer globally
    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Find the user-customer relationship
    user_customer = UserCustomer.query.filter_by(user_id=user.id, customer_id=customer.id).first()
    if not user_customer:
        return jsonify({"error": "Customer not linked to this business"}), 404

    # Delete the relationship (not the global customer record)
    db.session.delete(user_customer)
    db.session.commit()

    return jsonify({"success": True, "message": f"Customer {email} removed from your business."}), 200


@functionality.route('/customer-count', methods=['GET'])
def customer_count():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    count = UserCustomer.query.filter_by(user_id=user.id).count()
    return jsonify({"customer_count": count}), 200

@functionality.route('/edit-customer', methods=['PUT'])
def edit_customer():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    old_email = data.get('old_email')
    new_email = data.get('new_email')

    if not old_email or not new_email:
        return jsonify({"error": "Both old_email and new_email are required"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Find the customer globally
    customer = Customer.query.filter_by(email=old_email).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Check if this customer belongs to the current user
    user_customer = UserCustomer.query.filter_by(user_id=user.id, customer_id=customer.id).first()
    if not user_customer:
        return jsonify({"error": "Customer not linked to this business"}), 404

    # Check if the new email is already taken
    if Customer.query.filter_by(email=new_email).first():
        return jsonify({"error": "New email already exists"}), 400

    # Update the email
    customer.email = new_email
    db.session.commit()

    return jsonify({"success": True, "message": f"Customer email updated from {old_email} to {new_email}."}), 200


@functionality.route("/user_delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Delete the user (will also delete related objects if cascade is set up)
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print("Delete user error:", e)
        return jsonify({"error": "Server error"}), 500