from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # avoid reserved words like "user" in PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)  # increased for scrypt hashes

    customers = db.relationship('UserCustomer', back_populates='user', cascade="all, delete-orphan")
    menu_items = db.relationship('MenuItem', back_populates='business', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)

    users = db.relationship('UserCustomer', back_populates='customer', cascade="all, delete-orphan")


class UserCustomer(db.Model):
    __tablename__ = 'user_customers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete="CASCADE"), nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    last_reminder_sent = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='customers')
    customer = db.relationship('Customer', back_populates='users')


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    required_points = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    business = db.relationship('User', back_populates='menu_items')
