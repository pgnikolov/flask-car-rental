from flask import render_template
from flask_login import current_user
from . import views_bp

@views_bp.route('/')
def index():
    return render_template('home.html')