from flask import Flask, request, jsonify, render_template_string, redirect
import requests

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
    <h2>🌟 Facebook Auto Token Extractor (2025 Latest)</h2>

    <h3>🔹 Step 1: Get Cookies (Login with Facebook)</h3>
    <form action="/get_cookies" method="post">
        <label>Email / Phone:</label>
        <input type="text" name="email" required><br>
        <label>Password:</label>
        <input type="password" name="password" required><br>
        <input type="submit" value="Login & Get Cookies">
    </form>

    <hr>

    <h3>🔹 Step 2: Extract Token (Enter Cookies)</h3>
    <form action="/get_token" method="post">
        <label>Paste Your Cookies:</label>
        <textarea name="cookies" rows="5" required></textarea><br>
        <input type="submit" value="Extract Token">
    </form>

    <hr>

    <h3>🔹 Instagram Permission Access</h3>
    <a href='https://www.facebook.com/dialog/oauth?client_id=124024574287414&redirect_uri=https://business.facebook.com&scope=instagram_basic,instagram_manage_messages,pages_messaging' target='_blank'>
        <button>Give Instagram Permission</button>
    </a>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_cookies', methods=['POST'])
def get_cookies():
    email = request.form['email']
    password = request.form['password']

    # ✅ Step 1: Login and Get Cookies
    login_url = "https://m.facebook.com/login/device-based/validate-password/"
    session = requests.Session()
    
    # Fake Headers (Bypass Bot Detection)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile)",
        "Referer": "https://m.facebook.com/",
    }
    
    # Login Data
    login_data = {
        "email": email,
        "pass": password,
        "login": "Log In",
    }

    # Send Login Request
    response = session.post(login_url, data=login_data, headers=headers)

    # Check if Login Success
    if "c_user" in session.cookies.get_dict():
        cookies = "; ".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()])
        return f"""
            <h3>✅ Login Successful! Copy Your Cookies:</h3>
            <textarea rows='3'>{cookies}</textarea>
        """
    else:
        return "❌ Login Failed! Check Credentials."

@app.route('/get_token', methods=['POST'])
def get_token():
    cookies = request.form['cookies']

    # Convert cookies to dictionary
    cookies_dict = {}
    for line in cookies.split(";"):
        name, value = line.strip().split("=", 1)
        cookies_dict[name] = value

    headers = {
        "cookie": "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
    }

    # ✅ Step 2: Get Facebook User ID
    uid_url = "https://business.facebook.com/business_locations"
    response = requests.get(uid_url, headers=headers)
    
    if "EAA" not in response.text:
        return "❌ Failed to extract token. Invalid cookies or session expired."
    
    # ✅ Step 3: Extract EAAB Token
    token = response.text.split('EAA')[1].split('"')[0]
    token = "EAA" + token

    # ✅ Step 4: Validate Token Permissions
    permissions_url = f"https://graph.facebook.com/me/permissions?access_token={token}"
    permissions_response = requests.get(permissions_url)
    
    return f"""
        <h3>✅ Token Extracted Successfully!</h3>
        <textarea rows='3'>{token}</textarea>
        <hr>
        <h3>🔍 Permissions Status:</h3>
        <pre>{permissions_response.text}</pre>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
