from flask import Blueprint, render_template
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/panel')
@login_required
def user_panel():
    return render_template('user.html', current_user=current_user)
