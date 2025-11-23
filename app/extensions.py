from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Centralize extension instances in this file to avoid circular imports
db = SQLAlchemy()
migrate = Migrate()