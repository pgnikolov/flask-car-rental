from datetime import datetime
from flask import flash, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from app import db
from app.admin.routes import admin_required
from app.forms import RentalForm
from app.models import Car, RentalHistory
from app.rental import rentals_bp

@login_required
@rentals_bp.route('/rent/<int:car_id>', methods=['POST'])
def rent_car_route(car_id):
    user_id = current_user.id  # Get the logged-in user's ID
    if user_id is None:
        flash("Please log in to rent a car.")
        return redirect(url_for('auth.login'))

    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    pickup_location = request.form.get('pickup_location')
    return_location = request.form.get('return_location')

    return rent_car(user_id, car_id, start_date, end_date, pickup_location, return_location)


@login_required
@rentals_bp.route('/rent_form/<int:car_id>', methods=['GET'])
def rent_form(car_id):
    car = Car.query.get(car_id)
    if car:
        form = RentalForm()
        locations = [
            ('location_1', 'Location 1'),
            ('location_2', 'Location 2'),
            ('location_3', 'Location 3'),
        ]


        form.pickup_location.choices = locations
        form.return_location.choices = locations

        return render_template('rental.html', form=form, car_id=car_id)
    else:
        flash("Car not found.")
        return redirect(url_for('views.list_cars'))

# Function to process the rental logic
def rent_car(user_id, car_id, start_date, end_date, pickup_location, return_location):
    car = Car.query.get(car_id)
    if not car or not car.status:
        flash("Car is not available for rent.")
        return redirect(url_for('cars.list_cars'))
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    rental_days = (end_date - start_date).days
    if rental_days <= 0:
        flash("Invalid rental period.")
        return redirect(url_for('cars.list_cars'))

    rental_price_per_day = car.rental_price
    total_cost = rental_days * rental_price_per_day

    # Create a new rental record
    new_rental = RentalHistory(
        user_id=user_id,
        car_id=car_id,
        start_date=start_date,
        end_date=end_date,
        total_cost=total_cost,
        status='active',
        pickup_location=pickup_location,
        return_location=return_location
    )

    # Set car status to False (rented)
    car.status = False

    # Add to the session and commit
    db.session.add(new_rental)
    db.session.commit()

    flash("Car rented successfully!")
    return redirect(url_for('views.list_cars'))

# Route for returning a car
@admin_required
@login_required
@rentals_bp.route('/return/<int:rental_id>', methods=['POST'])
def return_car_route(rental_id):
    return return_car(rental_id)

# Function to process the return logic
def return_car(rental_id):
    rental = RentalHistory.query.get(rental_id)
    if rental and rental.status == 'active':
        # Calculate final cost based on actual rental duration
        actual_end_date = datetime.utcnow()
        rental_days = (actual_end_date - rental.start_date).days
        total_cost = rental_days * rental.car.rental_price

        # Update rental record
        rental.end_date = actual_end_date
        rental.total_cost = total_cost
        rental.status = 'completed'

        # Set car status back to True (available)
        rental.car.status = True

        # Commit changes
        db.session.commit()

        flash("Car returned successfully!")
    else:
        flash("Rental record not found or car already returned.")

    return redirect(url_for('views.list_cars'))
