import webbrowser
import http.server
import socketserver
import urllib.parse
import requests
import json
import os

# === Your eBay App Credentials ===
CLIENT_ID = "markelto-pokemonp-SBX-bf050fdfc-b2356712"
CLIENT_SECRET = "ZZZ"  # Replace with your real Cert ID
RUNAME = "mark_elton-markelto-pokemo-bhgdhik"
REDIRECT_URI = RUNAME

# === Scopes you need (keep minimal in sandbox) ===
SCOPES = [
    "https://api.ebay.com/oauth/api_scope",
    "https://api.ebay.com/oauth/api_scope/sell.inventory",
    "https://api.ebay.com/oauth/api_scope/sell.account",
    "https://api.ebay.com/oauth/api_scope/sell.fulfillment"
]

AUTH_URL = f"https://auth.sandbox.ebay.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={'%20'.join(SCOPES)}"
TOKEN_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"

# === Token save path (your working directory) ===
TOKEN_SAVE_PATH = "C:/Users/marke/Documents/program/ebay_token.json"

# === Local Web Server to Catch Redirect ===
class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)
        code = params.get("code")
        if code:
            self.send_response(200)
            self.end_headers()
            self.wfile.write("<h1>✅ Auth successful. You can close this tab.</h1>".encode("utf-8"))
            print("\n🔑 Authorization code received!")
            exchange_code_for_token(code[0])
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("<h1>❌ No code received</h1>".encode("utf-8"))

def exchange_code_for_token(code):
    print("📡 Exchanging code for access token...")
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(TOKEN_URL, data=data, headers=headers, auth=auth)
print(f"\n🔍 Status Code: {response.status_code}")
print(f"🔍 Raw Response: {response.text}")

if response.status_code == 200:
    token_data = response.json()
    os.makedirs(os.path.dirname(TOKEN_SAVE_PATH), exist_ok=True)
    with open(TOKEN_SAVE_PATH, "w") as f:
        json.dump(token_data, f, indent=2)
    print(f"✅ Access token saved to {TOKEN_SAVE_PATH}")
else:
    print("❌ Token exchange failed.")
        token_data = response.json()
        os.makedirs(os.path.dirname(TOKEN_SAVE_PATH), exist_ok=True)
        with open(TOKEN_SAVE_PATH, "w") as f:
            json.dump(token_data, f, indent=2)
        print(f"✅ Access token saved to {TOKEN_SAVE_PATH}")
    else:
        print("❌ Token exchange failed:")
        print(response.text)

# === Launch OAuth Flow ===
if __name__ == "__main__":
    print(f"🌐 Opening browser to authenticate...\n{AUTH_URL}")
    webbrowser.open(AUTH_URL)

    print("🚦 Waiting for redirect at localhost:8080...")
    with socketserver.TCPServer(("localhost", 8080), OAuthHandler) as httpd:
        httpd.handle_request()

