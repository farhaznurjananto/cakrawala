from flask import Flask, request, jsonify
from model import predict
from flask_cors import CORS
import json
# from model_ml import train_model, predict

app = Flask(__name__)
CORS(app)

# Dummy data
# data = [[1], [2], [3]]
# target = [2, 4, 6]

# Train the model
# model = train_model(data, target)

config = {
    "sandbox_server_key": "SB-Mid-server-EH1pOSzfaH-4HH2iZWeQ1tmo",
    "production_server_key": "prod-server-key",
    "sandbox_url": "https://app.sandbox.midtrans.com/snap/v1/transactions",
    "production_url": "https://app.midtrans.com/snap/v1/transactions",
    "is_production": "false",
}

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
#   return "Hello World!"
    try:
        # print(type(input_data))
        # return request.json['data']
        input_data = request.json['data']
        prediction = predict(input_data)
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)})

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
