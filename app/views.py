from flask import Blueprint, render_template
from flask_login import  current_user


views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('home.html', user=current_user)
