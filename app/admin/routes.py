from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import Car, CarType, FuelType, GearboxType
from app.forms import CarForm


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("You do not have permission to access the admin panel.", "danger")
            return redirect(url_for('user.user_panel'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_bp.route('/panel')
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html', current_user=current_user)


@admin_bp.route('/add_car', methods=['GET', 'POST'])
@login_required
@admin_required
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        new_car = Car(
            brand=form.brand.data,
            model=form.model.data,
            year=form.year.data,
            rental_price=form.rental_price.data,
            type=CarType[form.type.data],
            fuel=FuelType[form.fuel.data],
            gearbox=GearboxType[form.gearbox.data],
            color=form.color.data,
            seats=form.seats.data,  # New field for seats
            doors=form.doors.data,  # New field for doors
            mileage=form.mileage.data,  # New field for mileage
            status=True
        )
        db.session.add(new_car)
        db.session.commit()
        flash('Car added successfully!', 'success')
        return redirect(url_for('admin.admin_panel'))
    return render_template('add_car.html', form=form, current_user=current_user)


@admin_bp.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = CarForm(obj=car)

    if form.validate_on_submit():
        try:
            car.brand = form.brand.data
            car.model = form.model.data
            car.year = form.year.data
            car.rental_price = form.rental_price.data
            car.type = CarType[form.type.data]
            car.fuel = FuelType[form.fuel.data]
            car.gearbox = GearboxType[form.gearbox.data]
            car.color = form.color.data
            car.seats = form.seats.data
            car.doors = form.doors.data
            car.mileage = form.mileage.data

            db.session.commit()
            flash('Car updated successfully!', 'success')
            return redirect(url_for('admin.manage_cars'))
        except SQLAlchemyError as e:
            db.session.rollback()  # No changes will be aplied if there's an error
            flash('An error occurred while updating the car. Please try again.', 'danger')

    return render_template('edit_car.html', form=form, car=car, current_user=current_user)


@admin_bp.route('/manage_cars', methods=['GET', 'POST'])
@admin_required
@login_required
def manage_cars():
    all_cars = Car.query.all()

    if request.method == 'POST':
        car_id = request.form.get('car_id')
        car_to_delete = Car.query.get(car_id)
        if car_to_delete:
            db.session.delete(car_to_delete)
            db.session.commit()
            flash('Car deleted successfully!', 'success')
        else:
            flash('Car not found.', 'danger')

        edit_car_id = request.form.get('edit_car_id')
        if edit_car_id:
            return redirect(url_for('admin.edit_car', car_id=edit_car_id))

    all_cars = Car.query.all()  # Retrieve cars again after deletion
    return render_template('manage_cars.html', cars=all_cars, current_user=current_user)
