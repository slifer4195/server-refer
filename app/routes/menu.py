
# routes/menu.py
from flask import Blueprint, request, jsonify, session
from ..models import db, User, MenuItem

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu', methods=['POST'])
def create_menu_item():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get('item')
    price = data.get('price')
    points = data.get('required_points')

    if not name or price is None or points is None:
        return jsonify({"error": "Missing fields"}), 400

    if not (0 <= points <= 100):
        return jsonify({"error": "Points must be between 0 and 100"}), 400

    item = MenuItem(name=name, price=price, required_points=points, user_id=user_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({"success": True, "item_id": item.id}), 201

@menu_bp.route('/list_menu', methods=['GET'])
def list_menu_items():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    items = MenuItem.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "required_points": item.required_points
        } for item in items
    ])

@menu_bp.route('/update_menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    item = MenuItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    item.name = data.get('item', item.name)
    item.price = data.get('price', item.price)
    item.required_points = data.get('required_points', item.required_points)

    if not (0 <= item.required_points <= 100):
        return jsonify({"error": "Points must be between 0 and 100"}), 400

    db.session.commit()
    return jsonify({"success": True})

@menu_bp.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    item = MenuItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"success": True})