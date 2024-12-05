from flask import Flask
from stock_webapp.extensions import db
from stock_webapp.routes import routes

"""
This file is the main application for the Flask web app
It sets up configurations, initializes extensions, and registers blueprints
"""


def create_app():
    """
    Use to create and configure the Flask app

    Returns:
        A fully configured Flask app instance
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize extensions
    db.init_app(app)

    # register blueprints
    app.register_blueprint(routes)

    return app
