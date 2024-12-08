# stock_webapp/__init__.py
from flask import Flask
from stock_webapp.extensions import db
from stock_webapp.routes import routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(routes)

    return app
