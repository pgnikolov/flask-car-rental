from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
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
    all_cars = Car.query.all()
    return render_template('manage_cars.html', cars=all_cars, current_user=current_user)
