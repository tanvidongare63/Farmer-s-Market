from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    phone = db.Column(db.String(20))  # Add phone number field
    user_type = db.Column(db.String(20))  # 'farmer' or 'merchant'
    products = db.relationship('Product', backref='owner', lazy=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))
    base_price = db.Column(db.Float)
    image_path = db.Column(db.String(300))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bids = db.relationship('Bid', backref='product', lazy=True)

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 