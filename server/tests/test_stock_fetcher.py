import pytest
from unittest.mock import patch, MagicMock
from flask import jsonify
from api.stock_fetcher import AlphaVantageDemoFetcher
from api import app as flask_app

@pytest.fixture
def app():
    return flask_app 

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

@pytest.fixture
def fetcher():
    return AlphaVantageDemoFetcher()

def test_invalid_symbol(fetcher, app_context): 
    with patch('api.stock_fetcher.logging') as mock_logging:
        response, status_code = fetcher.fetch_symbol_data('INVALID')
        assert status_code == 403
        assert 'error' in response.get_json() 
        mock_logging.error.assert_called_once_with("Symbol INVALID not included in free version")

def test_no_symbol_provided(fetcher, app_context): 
    with patch('api.stock_fetcher.logging') as mock_logging:
        response, status_code = fetcher.fetch_symbol_data('')
        assert status_code == 400
        assert 'error' in response.get_json()
        mock_logging.error.assert_called_once_with("No stock symbol provided")

@patch('api.stock_fetcher.requests.get')
def test_valid_symbol(mock_get, fetcher, app_context):  
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "Time Series (Daily)": {
            "2022-01-01": {"4. close": "130"}
        }
    }
    mock_get.return_value = mock_response
    
    result = fetcher.fetch_symbol_data('IBM')
    assert 'dates' in result
    assert result['dates'] == ['2022-01-01']
    assert result['value'] == [130.0]
    mock_get.assert_called_once_with(
        'https://www.alphavantage.co/query',
        params={
            'function': 'TIME_SERIES_DAILY',
            'symbol': 'IBM',
            'outputsize': 'full',
            'apikey': 'demo'
        }
    )
