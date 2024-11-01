from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import CarType, FuelType, GearboxType


class CarForm(FlaskForm):
    """
    A Flask-WTF form for collecting and validating car data in the application.

    Fields:
        brand (StringField): The brand of the car.
        model (StringField): The model of the car.
        year (IntegerField): The manufacturing year of the car. Required.
        rental_price (IntegerField): The daily rental price for the car in currency units.
        type (SelectField): The type of car, with choices provided by the CarType Enum.
        fuel (SelectField): The fuel type of the car, with choices provided by the FuelType Enum.
        gearbox (SelectField): The gearbox type of the car, with choices provided by the GearboxType Enum.
        color (StringField): The color of the car. Required.
        seats (IntegerField): The number of seats in the car.
        doors (IntegerField): The number of doors on the car.
        mileage (IntegerField): The car’s mileage in kilometers.
        submit (SubmitField): Submit button to add a new car with the provided details.

    Validators:
        DataRequired: Ensures that each field has input from the user.
    """

    brand = StringField('Brand', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    rental_price = IntegerField('Rental Price', validators=[DataRequired()])
    type = SelectField('Type', choices=[(car_type.name, car_type.value) for car_type in CarType],
                       validators=[DataRequired()])
    fuel = SelectField('Fuel', choices=[(fuel_type.name, fuel_type.value) for fuel_type in FuelType],
                       validators=[DataRequired()])
    gearbox = SelectField('Gearbox', choices=[(gearbox_type.name, gearbox_type.value) for gearbox_type in GearboxType],
                          validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])

    # New fields added
    seats = IntegerField('Number of Seats', validators=[DataRequired()])
    doors = IntegerField('Number of Doors', validators=[DataRequired()])
    mileage = IntegerField('Mileage (in km)', validators=[DataRequired()])

    submit = SubmitField('Add Car')