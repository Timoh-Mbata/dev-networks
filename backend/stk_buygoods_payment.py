# Here we are handling payments integrated with stk safaricom buygoods
import requests
import base64
import json
from datetime import datetime
from flask import current_app

# Safaricom M-Pesa API credentials
CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
BUSINESS_SHORTCODE = "YOUR_TILL_NUMBER"  # Lipa na M-Pesa Till Number
PASSKEY = "YOUR_LIPA_NA_MPESA_PASSKEY"
CALLBACK_URL = "https://yourdomain.com/callback"

# Function to get M-Pesa Access Token
def get_access_token():
    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth = (CONSUMER_KEY, CONSUMER_SECRET)
    response = requests.get(url, auth=auth)
    return response.json().get("access_token")

# Function to initiate STK Push
def initiate_stk_push(phone_number, amount, mac_address):
    access_token = get_access_token()
    # Generate STK Push password
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": mac_address,
        "TransactionDesc": "Internet Access Payment"
    }

    response = requests.post("https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("CheckoutRequestID")
    else:
        return None
