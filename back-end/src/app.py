from .entities.entity import Session, engine, Base
from .docdict.docdict import init_dict, searchText
from flask import Flask, jsonify, request
from flask_cors import CORS

# creating the flask app
app = Flask(__name__)
CORS(app)

# generate database schema
# Base.metadata.create_all(engine)

@app.before_request
def before_request_handler():
    init_dict()

@app.route('/initial_text/<string:filename>', methods=['GET'])
def init_text(filename):
    try:
        with open(f'./doc/{filename}.txt', 'r') as file:
            content = file.read()
            return jsonify({"content": content}), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/search_text/<string:filename>/<string:searchContent>', methods=['GET'])
def search_text(filename, searchContent):
    try:
        response = searchText(filename, searchContent)
        return jsonify(response), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
