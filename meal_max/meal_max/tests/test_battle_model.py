import pytest

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

@pytest.fixture()
def battle_model():
    return PlaylistModel()


@pytest.fixture()
def mock_update_meal_stats(mocker):
    return mocker.patch("meal_max.models.battle_model.update_meal_stats")

@pytest.fixture()
def sample_meal1():
    return Meal()