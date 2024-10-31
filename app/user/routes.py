from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import RentalHistory, Car
from app import db
from datetime import datetime, timezone


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/panel')
@login_required
def user_panel():
    return render_template('user.html', current_user=current_user)


@user_bp.route('/rent/<int:car_id>', methods=['POST'])
@login_required
def rent_car(car_id):
    car = Car.query.get_or_404(car_id)

    if not car.status:  # If the car is not available
        flash("This car is already rented.", "danger")
        return redirect(url_for('views.list_cars'))

    # start and end date from the form
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    start_of_rent = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    end_of_rent = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

    if start_of_rent < datetime.now(timezone.utc):
        flash("Start date cannot be in the past.", "danger")
        return redirect(url_for('views.list_cars'))

    # new rental record
    rental = RentalHistory(
        user_id=current_user.id,
        car_id=car.id,
        start_of_rent=start_of_rent,
        end_of_rent=end_of_rent
    )
    db.session.add(rental)

    car.status = False
    db.session.commit()

    flash("You have successfully rented the car!", "success")

    return redirect(url_for('views.list_cars'))


@user_bp.route('/my_rentals', methods=['GET'])
@login_required
def my_rentals():
    rentals = RentalHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('my_rentals.html', rentals=rentals)