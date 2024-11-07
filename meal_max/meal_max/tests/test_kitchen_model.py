import pytest
import sqlite3
from unittest.mock import MagicMock, patch

from meal_max.models.kitchen_model import (
    Meal,
    create_meal,
    delete_meal,
    get_leaderboard,
    get_meal_by_id,
    get_meal_by_name,
    update_meal_stats
)

##################################################
# Fixtures
##################################################

@pytest.fixture
def mock_db_connection():
    """Mock database connection for testing."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

@pytest.fixture
def sample_meal():
    """Fixture providing a sample meal for testing."""
    return Meal(
        id=1,
        meal="Spaghetti Carbonara",
        cuisine="Italian",
        price=15.99,
        difficulty="MED"
    )

@pytest.fixture
def sample_leaderboard_data():
    """Fixture providing sample leaderboard data."""
    return [
        (1, "Spaghetti Carbonara", "Italian", 15.99, "MED", 10, 7, 0.7),
        (2, "Pizza Margherita", "Italian", 12.99, "LOW", 8, 5, 0.625)
    ]

##################################################
# Meal Class Tests
##################################################

def test_meal_creation_valid():
    """Test creating a valid meal object."""
    meal = Meal(1, "Spaghetti", "Italian", 15.99, "MED")
    assert meal.id == 1
    assert meal.meal == "Spaghetti"
    assert meal.cuisine == "Italian"
    assert meal.price == 15.99
    assert meal.difficulty == "MED"

def test_meal_creation_invalid_price():
    """Test creating a meal with invalid price raises ValueError."""
    with pytest.raises(ValueError, match="Price must be a positive value."):
        Meal(1, "Spaghetti", "Italian", -15.99, "MED")

def test_meal_creation_invalid_difficulty():
    """Test creating a meal with invalid difficulty raises ValueError."""
    with pytest.raises(ValueError, match="Difficulty must be 'LOW', 'MED', or 'HIGH'."):
        Meal(1, "Spaghetti", "Italian", 15.99, "INVALID")

##################################################
# Create Meal Tests
##################################################

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_create_meal_success(mock_get_db, mock_db_connection):
    """Test successful meal creation."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn

    create_meal("Spaghetti", "Italian", 15.99, "MED")
    
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_create_meal_duplicate(mock_get_db, mock_db_connection):
    """Test creating a duplicate meal raises ValueError."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.execute.side_effect = sqlite3.IntegrityError

    with pytest.raises(ValueError, match="Meal with name 'Spaghetti' already exists"):
        create_meal("Spaghetti", "Italian", 15.99, "MED")

def test_create_meal_invalid_price():
    """Test creating a meal with invalid price."""
    with pytest.raises(ValueError, match="Invalid price: -15.99. Price must be a positive number."):
        create_meal("Spaghetti", "Italian", -15.99, "MED")

def test_create_meal_invalid_difficulty():
    """Test creating a meal with invalid difficulty."""
    with pytest.raises(ValueError, match="Invalid difficulty level: INVALID. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal("Spaghetti", "Italian", 15.99, "INVALID")

##################################################
# Delete Meal Tests
##################################################

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_delete_meal_success(mock_get_db, mock_db_connection):
    """Test successful meal deletion."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchone.return_value = [False]

    delete_meal(1)
    
    assert mock_cursor.execute.call_count == 2
    mock_conn.commit.assert_called_once()

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_delete_meal_already_deleted(mock_get_db, mock_db_connection):
    """Test deleting an already deleted meal."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchone.return_value = [True]

    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        delete_meal(1)

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_delete_meal_not_found(mock_get_db, mock_db_connection):
    """Test deleting a non-existent meal."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Meal with ID 1 not found"):
        delete_meal(1)

##################################################
# Get Leaderboard Tests
##################################################

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_get_leaderboard_by_wins(mock_get_db, mock_db_connection, sample_leaderboard_data):
    """Test getting leaderboard sorted by wins."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchall.return_value = sample_leaderboard_data

    leaderboard = get_leaderboard(sort_by="wins")
    
    assert len(leaderboard) == 2
    assert leaderboard[0]['wins'] == 7
    assert leaderboard[0]['win_pct'] == 70.0

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_get_leaderboard_by_win_pct(mock_get_db, mock_db_connection, sample_leaderboard_data):
    """Test getting leaderboard sorted by win percentage."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchall.return_value = sample_leaderboard_data

    leaderboard = get_leaderboard(sort_by="win_pct")
    
    assert len(leaderboard) == 2
    assert leaderboard[0]['win_pct'] == 70.0

def test_get_leaderboard_invalid_sort():
    """Test getting leaderboard with invalid sort parameter."""
    with pytest.raises(ValueError, match="Invalid sort_by parameter"):
        get_leaderboard(sort_by="invalid")

##################################################
# Get Meal Tests
##################################################

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_get_meal_by_id_success(mock_get_db, mock_db_connection):
    """Test successfully retrieving a meal by ID."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchone.return_value = (1, "Spaghetti", "Italian", 15.99, "MED", False)

    meal = get_meal_by_id(1)
    assert isinstance(meal, Meal)
    assert meal.meal == "Spaghetti"

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_get_meal_by_name_success(mock_get_db, mock_db_connection):
    """Test successfully retrieving a meal by name."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchone.return_value = (1, "Spaghetti", "Italian", 15.99, "MED", False)

    meal = get_meal_by_name("Spaghetti")
    assert isinstance(meal, Meal)
    assert meal.id == 1

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_get_meal_by_id_deleted(mock_get_db, mock_db_connection):
    """Test retrieving a deleted meal by ID."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchone.return_value = (1, "Spaghetti", "Italian", 15.99, "MED", True)

    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        get_meal_by_id(1)

##################################################
# Update Meal Stats Tests
##################################################

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_update_meal_stats_win(mock_get_db, mock_db_connection):
    """Test updating meal stats for a win."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchone.return_value = [False]

    update_meal_stats(1, "win")
    
    assert mock_cursor.execute.call_count == 2
    mock_conn.commit.assert_called_once()

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_update_meal_stats_loss(mock_get_db, mock_db_connection):
    """Test updating meal stats for a loss."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn
    mock_cursor.fetchone.return_value = [False]

    update_meal_stats(1, "loss")
    
    assert mock_cursor.execute.call_count == 2
    mock_conn.commit.assert_called_once()

@patch('meal_max.models.kitchen_model.get_db_connection')
def test_update_meal_stats_invalid_result(mock_get_db, mock_db_connection):
    """Test updating meal stats with invalid result."""
    mock_conn, mock_cursor = mock_db_connection
    mock_get_db.return_value.__enter__.return_value = mock_conn

    mock_cursor.fetchone.return_value = (False,)  
    with pytest.raises(ValueError) as exc_info:
        update_meal_stats(1, "invalid")
    
    assert str(exc_info.value) == "Invalid result: invalid. Expected 'win' or 'loss'."


