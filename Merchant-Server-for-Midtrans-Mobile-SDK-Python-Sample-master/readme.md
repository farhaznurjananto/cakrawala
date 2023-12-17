Simple Merchant Server Implementation Reference for Mobile SDK (Python version).

## Description
This is a example mobile SDK server for Midtrans's iOS and Android SDK, as an implementation reference to use the mobile sdk.
Please read more in [Documentation of Midtrans mobile SDK](http://mobile-docs.midtrans.com/).

## Purpose
The main idea why this server implementation needed is: **To securely add HTTP Authorization Header** from server side.
This auth header is generated from **server key** (from your Midtrans account), this server key is secret, and should only be kept in server side, not client side (mobile app can be easily reverse engineered to extract any secret).

Additionally, it allows you to tweak JSON request parameter as needed from server side.

### Prerequisites
You need these to run the app:

* [Python 2.7.x](https://www.python.org/)

### Install dependencies
```bash
$ pip install -r requirements.txt
```

### Running the app
```bash
$ export FLASK_ENV=development
$ python app.py / flask run
```

## Endpoints
There is only one endpoint that are required to use Midtrans mobile SDK:

```
POST /charge
```

This endpoint will **proxy (forward)** client request to Midtrans Snap API `'https://app.midtrans.com/snap/v1/transactions'` (or `'https://app.sandbox.midtrans.com/snap/v1/transactions'` for sandbox) with **HTTP Authorization Header** generated based on your Midtrans `Server Key`.

The response of API will be printed/returned to client as is. Example response that will be printed

```
{
    "token": "413ae932-471d-4c41-bfb4-e558cc271dcc",
    "redirect_url": "https://app.sandbox.midtrans.com/snap/v2/vtweb/413ae932-471d-4c41-bfb4-e558cc271dcc"
}
```

## Usage
Edit file `config.yml`, insert your Midtrans Account Server Key to `sandbox_server_key` and `production_server_key`.
Set `is_production` to `True` when you use env production.

Set `<url where you host this>/charge` as `merchant base url` in mobile SDK. (refer to [Midtrans mobile SDK doc](https://mobile-docs.midtrans.com))


## Testing
You can mock client's request by executing this CURL command to the `/charge` endpoint:

```
curl -X POST \
   http://<your url>/charge \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "transaction_details": {
        "order_id": "mobile-12345",
        "gross_amount": 280000
    },
    "item_details": [
        {
            "id": "A01",
            "price": 280000,
            "quantity": 1,
            "name": "Mie Ayam Komplit"
        }
    ],
    "customer_details": [
        {
            "email": "tester@example.com",
            "first_name": "Budi",
            "last_name": "Khannedy",
            "phone": "628112341234"
        }
    ]
}'
```

Note: dont forget to change `"http://<your url>/charge"` to your url where you hosted the `/charge`.

You can also import that curl command to Postman.

## Notes
This is just for very basic implementation reference, in production, you should implement your backend more securely.

## Gopay Tokenization Merchant Server
For sample reference please refer to [this example](https://github.com/Midtrans/Merchant-Server-for-Midtrans-Mobile-SDK-Python-Sample/tree/master/tokenization-example) as it has a different specification.

### Get help
* [Midtrans&nbsp;](https://www.midtrans.com)
* [Midtrans registration](https://dashboard.midtrans.com/register)
* [Midtrans documentation](http://docs.midtrans.com)
* Can't find answer you looking for? email to [support@midtrans.com](mailto:support@midtrans.com)





