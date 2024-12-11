from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

"""
This file initializes Flask extensions used in the app, such as SQLAlchemy
Extensions are initialized here to allow modular app configuration
"""

db = SQLAlchemy()
migrate = Migrate()
