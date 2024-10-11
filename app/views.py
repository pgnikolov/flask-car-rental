from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Car, RentalHistory
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('home.html')
