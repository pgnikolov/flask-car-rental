from flask import Blueprint, render_template
from flask_login import  current_user
from app.models import Car
from app import db

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('home.html', user=current_user)

@views_bp.route('/cars', methods=['GET'])
def list_cars():
    all_cars = Car.query.all()
    return render_template('cars.html', cars=all_cars)