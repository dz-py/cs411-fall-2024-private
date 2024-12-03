import pytest
from unittest.mock import patch, Mock
import requests

from meal_max.utils.random_utils import get_random

##################################################
# Fixtures
##################################################

@pytest.fixture
def mock_response():
    """Fixture providing a mock requests response."""
    response = Mock()
    response.raise_for_status = Mock()
    return response

##################################################
# Test Cases
##################################################

@patch('requests.get')
def test_get_random_success(mock_get, mock_response):
    """Test successful random number retrieval."""
    mock_response.text = "0.42\n"
    mock_get.return_value = mock_response
    result = get_random()
    assert result == 0.42
    mock_get.assert_called_once_with(
        "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new",
        timeout=5
    )

@patch('requests.get')
def test_get_random_timeout(mock_get):
    """Test handling of timeout error."""
    mock_get.side_effect = requests.exceptions.Timeout()

    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()

@patch('requests.get')
def test_get_random_request_error(mock_get):
    """Test handling of general request error."""
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")

    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()

@patch('requests.get')
def test_get_random_invalid_response(mock_get, mock_response):
    """Test handling of invalid response format."""
    mock_response.text = "not_a_number\n"
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Invalid response from random.org: not_a_number"):
        get_random()

@patch('requests.get')
def test_get_random_http_error(mock_get, mock_response):
    """Test handling of HTTP error response."""
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="Request to random.org failed: 404 Client Error"):
        get_random()

@patch('requests.get')
def test_get_random_empty_response(mock_get, mock_response):
    """Test handling of empty response."""
    mock_response.text = "\n"
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Invalid response from random.org:"):
        get_random()

@patch('requests.get')
def test_get_random_whitespace_response(mock_get, mock_response):
    """Test handling of whitespace-only response."""
    mock_response.text = "   \n  "
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Invalid response from random.org:"):
        get_random(
