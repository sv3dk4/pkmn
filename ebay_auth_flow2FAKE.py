import requests
import webbrowser
import base64
import json
import os
from urllib.parse import urlencode

# === Configuration ===
client_id = "markelto-pokemonp-SBX-bf050fdfc-b2356712"
client_secret = "zzz"
redirect_uri = "mark_elton-markelto-pokemo-bhgdhik"
auth_code_url_base = "https://auth.ebay.com/oauth2/authorize"
token_url = "https://api.ebay.com/identity/v1/oauth2/token"
scopes = [
    "https://api.ebay.com/oauth/api_scope",
    "https://api.ebay.com/oauth/api_scope/sell.inventory",
    "https://api.ebay.com/oauth/api_scope/sell.account",
    "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
]

# === Token Save Path ===
save_path = "C:/Users/marke/Documents/program/ebay_token.json"

# === Step 1: Get User Authorization Code ===
params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": "code",
    "scope": " ".join(scopes)
}
auth_url = f"{auth_code_url_base}?{urlencode(params)}"
print(f"🔗 Visit this URL to authorize: {auth_url}")
webbrowser.open(auth_url)

# === Step 2: Paste Authorization Code ===
auth_code = input("Paste the authorization code from the URL: ").strip()

# === Step 3: Exchange for Access Token ===
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {encoded_credentials}"
}

data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": redirect_uri
}

response = requests.post(token_url, headers=headers, data=data)

# === Step 4: Save Token ===
if response.status_code == 200:
    token_data = response.json()
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)
    print(f"✅ Access token saved to: {save_path}")
else:
    print(f"❌ Failed to get token: {response.status_code}")
    print(response.text)
