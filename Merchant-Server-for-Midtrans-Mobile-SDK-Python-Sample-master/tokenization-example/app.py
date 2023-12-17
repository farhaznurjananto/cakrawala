import base64
import json

import requests
from flask import Flask
from flask import request

"""
This variable defines which port the test app is running at
"""
APPLICATION_PORT = 5000
"""
This defines which Midtrans API environment to target.
Set to `True` for production or `False` for Sandbox.
"""
IS_PRODUCTION = False

"""
Put your server key in this section accordingly to the environment
"""
server_key = {
    "sandbox": "sandbox-server-key",
    "production": "production-server-key"
}

host_url = {
    "sandbox": "https://api.sandbox.midtrans.com/v2",
    "production": "https://api.midtrans.com/v2"
}

partner_endpoint = {
    "account_linking": "/pay/account",
    "enquire_account": "/pay/account/{}",
    "create_transaction": "/charge",
    "unlink_account": "/pay/account/{}/unbind"
}


def get_environment():
    return "production" if IS_PRODUCTION else "sandbox"


def generate_auth_header_value():
    key = base64.b64encode(bytes(server_key[get_environment()], 'utf-8'))
    return "Basic {}".format(key.decode("ascii"))


def prepare_headers(json=True):
    header = {}
    if json:
        header["Content-Type"] = "application/json"
    header["Accept"] = "application/json"
    header["Authorization"] = generate_auth_header_value()
    return header


app = Flask(__name__)


@app.route("/v2/pay/account", methods=["POST"])
def link_account():
    body = request.json
    headers = prepare_headers()
    url = "{}{}".format(
        host_url[get_environment()],
        partner_endpoint["account_linking"]
    )
    api_response = requests.post(url, headers=headers, data=json.dumps(body))
    return api_response.json(), api_response.json().get("status_code")


@app.route("/v2/pay/account/<account_id>", methods=["GET"])
def enquire_account(account_id):
    headers = prepare_headers(json=False)
    endpoint = partner_endpoint["enquire_account"].format(account_id)
    url = "{}{}".format(
        host_url[get_environment()],
        endpoint
    )
    api_response = requests.get(url, headers=headers)
    return api_response.json(), api_response.json().get("status_code")


@app.route("/v2/charge", methods=["POST"])
def create_transaction():
    body = request.json
    headers = prepare_headers()
    url = "{}{}".format(
        host_url[get_environment()],
        partner_endpoint["create_transaction"]
    )
    if "idempotency-key" in request.headers:
        headers["Idempotency-Key"] = request.headers.get("Idempotency-Key")
    api_response = requests.post(url, headers=headers, data=json.dumps(body))
    return api_response.json(), api_response.json().get("status_code")


@app.route("/v2/pay/account/<account_id>/unbind", methods=["POST"])
def unlink_account(account_id):
    headers = prepare_headers()
    endpoint = partner_endpoint["unlink_account"].format(account_id)
    url = "{}{}".format(
        host_url[get_environment()],
        endpoint
    )
    api_response = requests.post(url, headers=headers)
    return api_response.json()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=APPLICATION_PORT)
