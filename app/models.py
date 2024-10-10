from . import db
from flask_login import UserMixin


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(150))
    model = db.Column(db.String(150))
    year = db.Column(db.Integer)
    rental_price = db.Column(db.Integer)
    type = db.Column(db.String(150))
    fuel = db.Column(db.String(150))
    gearbox = db.Column(db.String(150))
    color = db.Column(db.String(150))
    status = db.Column(db.Boolean, default=True)
    rented_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    start_of_rent = db.Column(db.DateTime, nullable=True)
    end_of_rent = db.Column(db.DateTime, nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))