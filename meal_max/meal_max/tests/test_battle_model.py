import pytest
from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

@pytest.fixture()
def battle_model():
    return BattleModel()

@pytest.fixture()
def mock_update_meal_stats(mocker):
    return mocker.patch("meal_max.models.battle_model.update_meal_stats")

@pytest.fixture()
def sample_meal1():
    return Meal(id=1, meal="Pasta", price=12.5, cuisine="Italian", difficulty="MED")  # Fill with realistic data

@pytest.fixture()
def sample_meal2():
    return Meal(id=2, meal="Sushi", price=15.0, cuisine="Japanese", difficulty="HIGH")  # Fill with realistic data

@pytest.fixture
def sample_battle(battle_model, sample_meal1, sample_meal2):
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    return [sample_meal1, sample_meal2]

def test_prep_combatant(battle_model, sample_meal1):
    battle_model.prep_combatant(sample_meal1)
    assert battle_model.get_combatants() == [sample_meal1]

def test_prep_combatant_max_capacity(battle_model, sample_meal1, sample_meal2):
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    with pytest.raises(ValueError, match="Combatant list is full"):
        battle_model.prep_combatant(Meal(id=3, meal="Tacos", price=10.0, cuisine="Mexican", difficulty="LOW"))

def test_battle_winner(battle_model, sample_battle, mock_update_meal_stats, mocker):
    mocker.patch("meal_max.utils.random_utils.get_random", return_value=0.1)
    winner = battle_model.battle()
    assert winner in [meal.meal for meal in sample_battle]
    assert len(battle_model.combatants) == 1  # to confirm whether the loser is removed
    assert mock_update_meal_stats.call_count == 2

def test_clear_combatants(battle_model, sample_meal1):
    battle_model.prep_combatant(sample_meal1)
    battle_model.clear_combatants()
    assert battle_model.get_combatants() == []

def test_get_battle_score(battle_model, sample_meal1):
    score = battle_model.get_battle_score(sample_meal1)
    assert isinstance(score, float)
    expected_score = (sample_meal1.price * len(sample_meal1.cuisine)) - {"HIGH": 1, "MED": 2, "LOW": 3}[sample_meal1.difficulty]
    assert score == expected_score

def test_battle_insufficient_combatants(battle_model):
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()
