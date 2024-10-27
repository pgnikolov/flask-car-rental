from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Function to check if the user is an admin
def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:  # Assuming an `is_admin` attribute on the user model
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
