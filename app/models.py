from . import db
from flask_login import UserMixin
from enum import Enum

class CarType(Enum):
    SUV = "SUV"
    SEDAN = "Sedan"
    HATCHBACK = "Hatchback"
    MINIVAN = "Minivan"
    COUPE = "Coupe"
    PICKUP = "Pickup"
    VAN = "Van"
    WAGON = "Wagon"

class FuelType(Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    ELECTRIC = "Electric"
    HYBRID = "Hybrid"

class GearboxType(Enum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"
    SEMI_AUTOMATIC = "Semi-automatic"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(150))
    model = db.Column(db.String(150))
    year = db.Column(db.Integer)
    rental_price = db.Column(db.Integer)
    type = db.Column(db.Enum(CarType), nullable=False)
    fuel = db.Column(db.Enum(FuelType), nullable=False)
    gearbox = db.Column(db.Enum(GearboxType), nullable=False)
    color = db.Column(db.String(150))
    status = db.Column(db.Boolean, default=True)
    rental_history = db.relationship('RentalHistory', backref='car', lazy=True)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    rented_cars = db.relationship('RentalHistory', backref='user', lazy=True)


class RentalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    start_of_rent = db.Column(db.DateTime, nullable=False)
    end_of_rent = db.Column(db.DateTime, nullable=True)
