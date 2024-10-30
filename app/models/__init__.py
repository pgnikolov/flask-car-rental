from enum import Enum
from flask_login import UserMixin
from app import db

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
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(150))
    model = db.Column(db.String(150))
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    doors = db.Column(db.Integer)
    seats = db.Column(db.Integer)
    rental_price = db.Column(db.Integer)
    type = db.Column(db.Enum(CarType), nullable=False)
    fuel = db.Column(db.Enum(FuelType), nullable=False)
    gearbox = db.Column(db.Enum(GearboxType), nullable=False)
    color = db.Column(db.String(150))
    status = db.Column(db.Boolean, default=True)
    rental_history = db.relationship('RentalHistory', backref='car', lazy=True)

class RentalHistory(db.Model):
    __tablename__ = 'rental_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    start_of_rent = db.Column(db.DateTime, nullable=False)
    end_of_rent = db.Column(db.DateTime, nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    rented_cars = db.relationship('RentalHistory', backref='user', lazy=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'
