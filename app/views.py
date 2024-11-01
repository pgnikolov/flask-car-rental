from flask import Blueprint, render_template, url_for
from flask_login import current_user
from app.models import Car


views_bp = Blueprint('views', __name__)


@views_bp.route('/')
def index():
    """
    Renders the home page. If the user is logged in, the template will
    display information specific to the logged-in user.
    Returns:
        Rendered template for 'home.html'.

    """
    return render_template('home.html', user=current_user)

@views_bp.route('/cars', methods=['GET'])
def list_cars():
    """
    Renders a list of cars, customized for the user type.
    Assigns a URL for each car's image to be displayed in the template.
    Uses a default image if the car does not have an `image_filename`.
    For Admin Users:
        - Shows all cars, regardless of availability.

    For Regular Users:
        - Shows only available cars (`status=True`).

    Returns:
        Rendered template for 'cars.html' with all available cars and
        their image URLs.

    """
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
