# Merchant Server Example For Gopay Tokenization SDK

## Overview

This is the merchant server example for Gopay Tokenization SDK.

In general the merchant server will pass all the request body and header to Partner API. The only change is to embed the `Server Key` that is base64 encoded into the request header as an authorization header.

The endpoint served are for:

* Account Linking
* Account Status Enquiry
* Create Transactions
* Unlinking Account

## Requirements

Requirements to run this example server are:

* Python 3.5+
* Virtualenv
* Valid Midtrans Server Key

## Running

* Setup virtual environment by running `$ virtualenv env`
* Activate virtual environment `$ source env/bin/activate`
* Install requirements `$ pip install -r requirements.txt`
* Put your server key in the server key section in `app.py`
* Run the server `$ python app.py`

The server will run on port 5000 by default. You can configure this in `app.py` in the `APPLICATION_PORT` variable.

## Usage with SDK

Put the merchant URL in the SDK init pointing to where you host this server and the SDK will function accordingly

## Notes
This is just for very basic implementation reference, in production, you should implement your backend more securely.

### Get help
* [Midtrans&nbsp;](https://www.midtrans.com)
* [Midtrans registration](https://dashboard.midtrans.com/register)
* [Midtrans documentation](http://docs.midtrans.com)
* Can't find answer you looking for? email to [support@midtrans.com](mailto:support@midtrans.com)

