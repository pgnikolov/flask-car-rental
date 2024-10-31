from flask import Blueprint, render_template, url_for
from flask_login import current_user
from app.models import Car


views_bp = Blueprint('views', __name__)


@views_bp.route('/')
def index():
    return render_template('home.html', user=current_user)

@views_bp.route('/cars', methods=['GET'])
def list_cars():
    if current_user.is_admin:
        # Admin sees all cars
        all_cars = Car.query.all()
    else:
        # users see only available cars
        all_cars = Car.query.filter_by(status=True).all()

    default_image = 'app/static/images/default.png'

    for car in all_cars:
        if car.image_filename:
            car.image_url = url_for('static', filename='images/' + car.image_filename)
        else:
            car.image_url = url_for('static', filename=default_image)
    return render_template('cars.html', cars=all_cars)
