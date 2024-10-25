from flask import render_template, redirect, url_for, flash, request
from app.models import User
from app.extensions.database import db
from . import rentals_bp
from flask_login import current_user

@rentals_bp.route('/rentals')
def list_cars():
    rented_cars = RentlHistory.query.filter_by(end_of_rent=None).all()
    rented_cars_ids = [rental.car_id for rental in rented_cars]
    available_cars = Car.query.filter(~Car.id.in_(rented_cars_ids)).all()
    return render_template('cars.html', cars=available_cars, user=current_user)

@rentals_bp.route('/add_rental', methods=['GET', 'POST'])
def add_rental():
    if request.method == 'POST':
        new_rental = Rental(
            car_id=request.form['car_id'],
            user_id=request.form['user_id'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date']
        )
        db.session.add(new_rental)
        db.session.commit()
        flash('Rental added successfully!', 'success')
        return redirect(url_for('rentals.list_rentals'))
    return render_template('rentals/add_rental.html')
