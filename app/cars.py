from flask import render_template, Blueprint
from flask_login import  current_user
from .models import Car, RentalHistory


cars_bp = Blueprint('cars', __name__)

@cars_bp.route('/cars')
def list_cars():
    rented_cars = RentalHistory.query.filter_by(end_of_rent=None).all()
    rented_cars_ids = [rental.car_id for rental in rented_cars]
    available_cars = Car.query.filter(~Car.id.in_(rented_cars_ids)).all()
    return render_template('cars.html', cars=available_cars, user=current_user)

