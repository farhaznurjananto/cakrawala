from flask import Flask
from flask import jsonify
from flask import request
import json
import requests
import yaml

app = Flask(__name__)

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)


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
    app.run(debug=True, host='0.0.0.0', port=config['app_port'])
