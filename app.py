import requests
import json
from flask import Flask, render_template_string, request, jsonify
from http.cookiejar import MozillaCookieJar

# Initialize Flask app
app = Flask(__name__)

# Initialize session to handle cookies
session = requests.Session()
session.cookies = MozillaCookieJar('cookies.txt')  # File where cookies will be stored

# User-Agent to mimic real browser behavior
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Home page route with HTML embedded
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Token Extractor</title>
    </head>
    <body>
        <h1>Token Extractor</h1>

        <h2>Extract Token from Cookies</h2>
        <form action="/extract_token" method="POST">
            <textarea name="cookies" rows="10" cols="50" placeholder="Paste your cookies here..."></textarea><br><br>
            <input type="submit" value="Extract Token">
        </form>
    </body>
    </html>
    ''')

# Extract token from cookies
@app.route('/extract_token', methods=['POST'])
def extract_token():
    cookies_data = request.form['cookies']
    
    # Save cookies to a file
    with open('cookies.txt', 'w') as f:
        f.write(cookies_data)
    
    # Load cookies into session
    session.cookies.load()
    
    # Extract EAAB token from cookies
    token = get_eaab_token_from_cookies()
    
    if token:
        if check_token_validity(token):
            return jsonify({"message": "Token is valid!", "token": token})
        else:
            return jsonify({"message": "Token is invalid or expired."})
    else:
        return jsonify({"message": "Failed to extract token."})

# Extract EAAB token from cookies (latest logic using Graph API v21.0)
def get_eaab_token_from_cookies():
    cookies_dict = session.cookies.get_dict()
    
    # EAAB token is usually stored in 'fbm_*' or 'c_user'
    if 'fbm_' in cookies_dict:
        return cookies_dict['fbm_']  # Return EAAB token (or adjust based on cookies)
    else:
        return None

# Check token validity using Graph API v21.0
def check_token_validity(token):
    validation_url = f"https://graph.facebook.com/v21.0/me?access_token={token}"
    response = session.get(validation_url, headers=headers)
    
    if response.status_code == 200:
        return True  # Token is valid
    else:
        return False  # Token is invalid or expired

# Define host and port for Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
