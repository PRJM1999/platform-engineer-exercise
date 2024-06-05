from flask_restful import Api, Resource
from flask import Flask, request, jsonify, make_response, send_from_directory, send_file


data_fetcher = Api()

class DataFetcher(Resource):

    def get(self):

        return jsonify("Hello World!")

data_fetcher.add_resource(DataFetcher, "/load_data")