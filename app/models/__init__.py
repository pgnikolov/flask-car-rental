from enum import Enum
from flask_login import UserMixin
from app import db


class CarType(Enum):
    """Enumeration for various car types."""

    SUV = "SUV"
    SEDAN = "Sedan"
    HATCHBACK = "Hatchback"
    MINIVAN = "Minivan"
    COUPE = "Coupe"
    PICKUP = "Pickup"
    VAN = "Van"
    WAGON = "Wagon"


class FuelType(Enum):
    """Enumeration for different fuel types available for cars."""

    PETROL = "Petrol"
    DIESEL = "Diesel"
    ELECTRIC = "Electric"
    HYBRID = "Hybrid"


class GearboxType(Enum):
    """Enumeration for gearbox types in vehicles."""

    MANUAL = "Manual"
    AUTOMATIC = "Automatic"
    SEMI_AUTOMATIC = "Semi-automatic"


class Car(db.Model):
    """Database model for a car available for rental."""

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
    image_filename = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=True)
    rental_history = db.relationship('RentalHistory', backref='car', lazy=True)


class RentalHistory(db.Model):
    """Database model for the rental history of cars."""

    __tablename__ = 'rental_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    start_of_rent = db.Column(db.DateTime, nullable=False)
    end_of_rent = db.Column(db.DateTime, nullable=True)


class User(db.Model, UserMixin):
    """Database model for a user in the car rental system."""

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
        """Represent the User instance by email."""

        return f'<User {self.email}>'
