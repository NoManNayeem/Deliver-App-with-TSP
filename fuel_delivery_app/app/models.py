from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'customer', 'admin', 'delivery_person'
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username} (Role: {self.role})>"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    fuel_quantity = db.Column(db.Integer, nullable=False)
    time_window_start = db.Column(db.DateTime, nullable=False)
    time_window_end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'assigned', 'delivered'
    assigned_to = db.Column(db.Integer, db.ForeignKey('delivery_person.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.id} (Customer: {self.customer.username}, Status: {self.status})>"

class DeliveryPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    vehicle_capacity = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref='delivery_person', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DeliveryPerson {self.name} (Capacity: {self.vehicle_capacity}L)>"
