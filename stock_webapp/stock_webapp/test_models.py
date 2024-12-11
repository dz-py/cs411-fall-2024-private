import pytest
from stock_webapp import create_app
from stock_webapp.extensions import db
from stock_webapp.models import User, Holding


@pytest.fixture
def app():
    """Fixture to create and configure the Flask app."""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.config['TESTING'] = True  
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def session(app):
    """Fixture to provide a session scoped to the test."""
    with app.app_context():
        yield db.session


@pytest.fixture
def new_user(session):
    """Fixture to create a new user."""
    user = User(username="testuser", password="testpassword")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def new_holding(new_user, session):
    """Fixture to create a new holding for the user."""
    holding = Holding(user_id=new_user.id, symbol="AAPL", quantity=10, price_per_share=150.0, total_cost=1500.0)
    session.add(holding)
    session.commit()
    return holding


def test_user_init(app, session, new_user):
    """Test the User __init__ method."""
    with app.app_context():
        user = session.get(User, new_user.id)  # Re-fetch the user within an active session
        assert user.username == "testuser"
        assert user.password_hash is not None
        assert user.salt is not None
        assert len(user.salt) == 64 


def test_generate_salt(app, session, new_user):
    """Test the generate_salt method."""
    with app.app_context():
        user = session.get(User, new_user.id)  # Re-fetch the user within an active session
        salt = user.generate_salt()
        assert len(salt) == 64
