from flask_restful import Api, Resource
from flask import Flask, request, jsonify, make_response, send_from_directory, send_file
from api.stock_fetcher import AlphaVantageDemoFetcher


data_fetcher = Api()

class DataRetrieval(Resource):

    def get(self):
        """
        Retrieve stock data for a specified symbol provided via query parameters.

        Returns:
            flask.Response: JSON-formatted stock data or error message with an HTTP status code.

        Examples:
            - GET /load_data?symbol=IBM returns JSON data for 'IBM'.
            - GET /load_data without a symbol returns error JSON {'error': 'No stock symbol provided'} with a 400 status.
        """
        symbol = request.args.get('symbol')
        fetcher = AlphaVantageDemoFetcher()
        result = fetcher.fetch_symbol_data(symbol)

        # Handle Errors
        if isinstance(result, tuple):
            return result 
        
        return jsonify(result)
    

data_fetcher.add_resource(DataRetrieval, "/load_data")