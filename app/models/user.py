from flask_login import UserMixin
from app.extensions.database import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    rented_cars = db.relationship('RentalHistory', backref='user', lazy=True)
    rentals = db.relationship('Rental', back_populates='user', lazy='dynamic')
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'
