from flask import render_template
from flask_login import current_user
from app.models import Car
from app import db
from . import cars_bp


# @cars_bp.route('/cars', methods=['GET'])
# def list_cars():
#     all_cars = Car.query.all()
#     return render_template('cars.html', cars=all_cars, user=current_user)