from abc import ABC, abstractmethod
import requests
from flask import jsonify
import logging
from datetime import datetime

class StockDataFetcher(ABC):
    
    @abstractmethod
    def fetch_symbol_data(self, symbol):
        """
        Fetch stock data for the given symbol.
        This method must be implemented by all subclasses.
        """
        pass

class AlphaVantageDemoFetcher(StockDataFetcher):
    """
    Implements stock data retrieval for demo allowed content using the AlphaVantage API.

    Attributes:
        API_URL (str): The endpoint URL for the AlphaVantage API.
        API_KEY (str): API key used for authenticating requests to AlphaVantage; set to 'demo'.
        ALLOWED_SYMBOLS (set): A set of stock symbols that are permitted for data fetching in the demo version.
    """
    API_URL = "https://www.alphavantage.co/query"
    API_KEY = 'demo'
    ALLOWED_SYMBOLS = {'IBM', 'TSCO.LON', 'SHOP.TRT', 'GPV.TRV', 'MBG.DEX', 'RELIANCE.BSE', '600104.SHH', '000002.SHZ'}


    def fetch_symbol_data(self, symbol: str) -> object:
        """
        Retrieves daily time series stock data for a specified symbol using the AlphaVantage API.

        Args:
            symbol (str): The stock symbol for which data is requested. Must be one of the allowed symbols.

        Returns:
            dict: A dictionary containing 'dates' and 'value' keys with lists of dates and closing prices respectively.
            tuple: A tuple containing a Flask `jsonify` response object and an HTTP status code, if an error occurs.

        Raises:
            400: If no symbol is provided.
            403: If the requested symbol is not included in the ALLOWED_SYMBOLS.
            404: If the data for the requested symbol is not found in the API response.

        Notes:
            Logging is used to provide informational, warning, and error messages depending on the function execution and outcome.
        """

        logging.info(f"Fetching data for symbol: {symbol}")
        
        if not symbol:
            logging.error("No stock symbol provided")
            return jsonify({'error': 'No stock symbol provided'}), 400
        if symbol not in self.ALLOWED_SYMBOLS:
            logging.error(f"Symbol {symbol} not included in free version")
            return jsonify({'error': 'Symbol not included in free version'}), 403

        # Make Request
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'full',
            'apikey': self.API_KEY
        }
        response = requests.get(self.API_URL, params=params)
        data = response.json()

        if 'Time Series (Daily)' not in data:
            logging.warning(f"No 'Time Series (Daily)' found in response for {symbol}")
            return jsonify({'error': 'No data available'}), 404


        # Extract close prices from response
        time_series_data = data.get('Time Series (Daily)', {})

        date_data = []
        value_data = []
        for date, details in time_series_data.items():
            date_data.append(date)
            value_data.append(float(details['4. close']))

        return {"dates": date_data, "value": value_data}