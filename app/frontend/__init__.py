from flask import Blueprint

# Create blueprint for frontend
frontend_bp = Blueprint('frontend', __name__,
                       template_folder='templates',
                       static_folder='static')

from . import routes