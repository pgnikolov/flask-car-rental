from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import views_bp

@views_bp.route('/')
def index():
    return render_template('home.html', current_user=current_user)
