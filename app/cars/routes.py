from flask import render_template
from flask_login import current_user
from app.models.car import Car
from app.models.rental import RentalHistory
from . import cars_bp


@cars_bp.route('/cars')
def list_cars():
    rented_cars = RentalHistory.query.filter_by(end_of_rent=None).all()
    rented_cars_ids = [rental.car_id for rental in rented_cars]
    available_cars = Car.query.filter(~Car.id.in_(rented_cars_ids)).all()
    return render_template('cars/list_cars.html', cars=available_cars, user=current_user)
