from flask import Flask, render_template, request, jsonify
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Selenium Configuration for Headless Chrome
def get_facebook_cookies():
    options = Options()
    options.add_argument("--headless")  # Headless Mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-data-dir=/tmp/chrome-data")  # Persistent Login

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.facebook.com/")

    cookies = driver.get_cookies()
    driver.quit()

    # Convert Cookies to JSON String
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    return json.dumps(cookie_dict)

# Home Page
@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>🔥 RAJ X DARK - Facebook Token Extractor 🔥</title>
        <style>
            body { background-color: black; color: lime; text-align: center; font-family: Arial; }
            h1 { color: red; }
            button { background-color: red; color: white; padding: 10px; border: none; cursor: pointer; margin: 10px; }
            textarea { width: 80%; height: 100px; }
        </style>
        <script>
            function copyText(id) {
                var text = document.getElementById(id);
                text.select();
                document.execCommand("copy");
                alert("Copied!");
            }

            function autoExtractCookies() {
                fetch('/extract_cookies')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('cookies').value = data.cookies || "Error Extracting Cookies!";
                });
            }
        </script>
    </head>
    <body>
        <h1>🔥 RAJ X DARK - Facebook Token Extractor 🔥</h1>

        <button onclick="autoExtractCookies()">🔥 Auto Extract Cookies</button><br><br>

        <h3>Paste Your Facebook Cookies:</h3>
        <textarea id="cookies"></textarea><br>
        <button onclick="extractToken()">Extract Token</button><br><br>

        <h3>Your Facebook Token:</h3>
        <textarea id="token" readonly></textarea><br>
        <button onclick="copyText('token')">📋 Copy Token</button><br><br>

        <button onclick="logout()">🔴 Logout from Facebook</button>

        <script>
            function extractToken() {
                var cookies = document.getElementById('cookies').value;
                fetch('/get_token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cookies: cookies })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('token').value = data.token || "Error: Invalid Cookies!";
                });
            }

            function logout() {
                fetch('/logout')
                .then(response => alert("Facebook Logged Out!"))
                .catch(error => alert("Error Logging Out!"));
            }
        </script>
    </body>
    </html>
    '''

# Route to Extract Cookies Automatically
@app.route('/extract_cookies')
def extract_cookies():
    cookies = get_facebook_cookies()
    return jsonify({"cookies": cookies})

# Token Extractor Route
@app.route('/get_token', methods=['POST'])
def get_token():
    data = request.json
    cookies = data.get("cookies", "")

    if not cookies:
        return jsonify({"error": "Cookies Required!"})

    # Convert Cookies to JSON Format
    try:
        cookie_dict = json.loads(cookies)
    except:
        return jsonify({"error": "Invalid Cookie Format!"})

    # Facebook Token Request
    response = requests.get("https://business.facebook.com/business_locations", cookies=cookie_dict).text
    token_start = response.find('EAAB')
    token_end = response.find('ZDZD') + 4

    if token_start != -1 and token_end != -1:
        token = response[token_start:token_end]
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid Cookies or No Token Found!"})

# Facebook Logout Route
@app.route('/logout')
def logout():
    return '''
    <script>
        document.cookie = "c_user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "xs=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        alert("Facebook Logged Out!");
        window.location.href = "/";
    </script>
    '''

# Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
