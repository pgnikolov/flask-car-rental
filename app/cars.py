from flask import render_template, Blueprint
from .models import Car
from . import db

cars_bp = Blueprint('cars', __name__)

@cars_bp.route('/cars')
def list_cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)

# Other routes and functions related to cars can be defined here
