from flask import Flask 
from flask_cors import CORS
from api.data_fetcher import data_fetcher

# Create App
app = Flask(__name__)

# Initialise API
data_fetcher.init_app(app)

# Enable CORS
CORS(app)


@app.route('/')
def index():
    """
    Test route to check server is running.
    """
    return "Server is running"