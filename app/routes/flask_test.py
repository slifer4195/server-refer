from sqlalchemy import inspect
from flask import Blueprint, render_template, session, request , redirect
from ..models import db, User, Customer, MenuItem


api_bp = Blueprint('api_test', __name__)

@api_bp.route("/db-inspect", methods=['GET'])
def db_inspect():
    print("test")
    inspector = inspect(db.engine)
    tables = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        tables[table_name] = columns  # list of dicts with column info
    return render_template("db_inspect.html", tables=tables)

@api_bp.route("/register-inspect", methods=["GET"])
def register():
    return render_template("register.html")

@api_bp.route("/login-inspect", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@api_bp.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login-inspect")

    user = User.query.get(user_id)
    customers = Customer.query.all()
    menu_items = MenuItem.query.filter_by(user_id=user_id).all()

    return render_template("dashboard.html", user=user, customers=customers, menu_items=menu_items)
