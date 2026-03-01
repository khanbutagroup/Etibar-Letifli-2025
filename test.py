import requests
from requests.auth import HTTPBasicAuth
import uuid

url = "https://preapi.birpay.az/v1/payments"

payload = {
    "amount": "1.00",
    "currency": "AZN",
    "description": "Test payment",
    "orderId": str(uuid.uuid4()),
    "confirmation": {
        "type": "REDIRECT",
        "returnUrl": "https://example.com"
    },
    "callbackUrl": "https://example.com",
    "posDetail": {
        "merchantId": "E1040009",
        "terminalId": "E1040009"
    }
}

headers = {
    "Content-Type": "application/json",
    "X-Idempotency-Key": str(uuid.uuid4())
}

r = requests.post(
    url,
    json=payload,
    headers=headers,
    auth=HTTPBasicAuth("click2birpay", "osvYshwOn158zUpay4pE5G6U1QWrKuHh")
)

print(r.status_code)
print(r.text)
