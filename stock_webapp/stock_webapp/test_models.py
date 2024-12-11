import pytest
from stock_webapp import create_app
from stock_webapp.extensions import db
from stock_webapp.models import User, Holding
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    with app.app_context(): 
        db.create_all() 
    yield app
    with app.app_context():
        db.drop_all() 

@pytest.fixture
def new_user(app):
    """Fixture to create a new user"""
    user = User(username="testuser", password="testpassword")
    with app.app_context():  
        db.session.add(user)
        db.session.commit()
    return user

@pytest.fixture
def new_holding(new_user, app):
    """Fixture to create a new holding for the user"""
    holding = Holding(user_id=new_user.id, symbol="AAPL", quantity=10, price_per_share=150.0, total_cost=1500.0)
    with app.app_context():
        db.session.add(holding)
        db.session.commit()
    return holding

def test_user_init(new_user):
    """Test the User __init__ method"""
    user = new_user
    assert user.username == "testuser"
    assert user.password_hash is not None
    assert user.salt is not None
    assert len(user.salt) == 64 
    
def test_generate_salt(new_user):
    """Test the generate_salt method"""
    user = new_user
    salt = user.generate_salt()
    assert len(salt) == 64 