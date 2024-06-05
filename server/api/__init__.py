from flask import Flask 
from flask_cors import CORS
from api.data_retrieval import data_fetcher
import logging

# Create App
app = Flask(__name__)

# Initialise API
data_fetcher.init_app(app)

# Enable CORS
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/')
def index():
    """
    Test route to check server is running.
    """
    return "Server is running"