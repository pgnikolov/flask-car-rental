from flask import Blueprint

rentals_bp = Blueprint('rentals', __name__)

from . import routes
