from flask import Blueprint

# Create blueprint for API endpoints
api_bp = Blueprint('api', __name__)

# Import and register route definitions with blueprint
from . import routes