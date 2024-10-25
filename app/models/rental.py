from datetime import datetime
from app.extensions.database import db
from .car import Car

class RentalHistory(db.Model):
    __tablename__ = 'rental_history'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    start_of_rent = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_of_rent = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active')

    def __init__(self, user_id, car_id):
        self.user_id = user_id
        self.car_id = car_id
        self.start_of_rent = datetime.now()
        self.end_of_rent = None
        self.status = 'active'

    def __repr__(self):
        return f'<Rental {self.id} - User: {self.user_id}, Car: {self.car_id}>'

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def is_active(self):
        return self.status == 'active'

    def complete_rental(self):
        self.status = 'completed'
        self.end_of_rent = datetime.now()
        db.session.commit()
