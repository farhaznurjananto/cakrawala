from flask import Flask, request, jsonify
from model import predict
from flask_cors import CORS
import json
import requests
import yaml

app = Flask(__name__)
CORS(app)

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

@app.route('/charge', methods=['post'])
def index():
    body = request.get_json()
    response = chargeAPI(body)

    return jsonify(response)

def chargeAPI(body):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = config['production_url'] if config['is_production'] else config['sandbox_url']
    server_key = config['production_server_key'] if config['is_production'] else config['sandbox_server_key']

    response = requests.post(url, headers=headers, auth=(server_key, ''), data=json.dumps(body))
    return response.json()

@app.route('/predict', methods=['POST'])
def hello():

    try:
        input_data = request.json['data']
        prediction = predict(input_data)
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
