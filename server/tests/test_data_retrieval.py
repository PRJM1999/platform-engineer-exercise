import pytest
from flask import Flask
from flask_restful import Api
from api.data_retrieval import DataRetrieval 

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(DataRetrieval, "/load_data")
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def app_context(app):
    """Create an application context before running the tests."""
    with app.app_context():
        yield

def test_data_retrieval_no_symbol(client, app_context):
    """Test retrieving data without providing a symbol."""
    response = client.get('/load_data')
    assert response.status_code == 500
