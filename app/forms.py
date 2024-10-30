from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import CarType, FuelType, GearboxType


class CarForm(FlaskForm):
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