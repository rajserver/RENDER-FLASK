from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

# Convert normal cookies to JSON format
def convert_cookies_to_json(raw_cookies):
    try:
        cookies_dict = {}
        for item in raw_cookies.split("; "):
            key, value = item.split("=", 1)
            cookies_dict[key] = value
        return json.dumps(cookies_dict)
    except:
        return None

# Grant Instagram permissions
def grant_instagram_permissions(cookies):
    try:
        headers = {
            "Cookie": cookies,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/91.0.4472.164 Mobile Safari/537.36"
        }
        insta_auth_url = "https://www.facebook.com/dialog/oauth?client_id=124024574287414&redirect_uri=https://www.instagram.com/&scope=instagram_basic,instagram_manage_messages"
        response = requests.get(insta_auth_url, headers=headers, allow_redirects=True)

        return "access_token=" in response.url
    except:
        return False

# Extract token from JSON cookies
def extract_token_from_cookies(json_cookies):
    try:
        cookies = json.loads(json_cookies)
        cookie_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])

        headers = {
            "Cookie": cookie_str,
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/91.0.4472.164 Mobile Safari/537.36"
        }

        response = requests.get("https://business.facebook.com/business_locations/", headers=headers)
        token_start = response.text.find('EAAB')

        if token_start != -1:
            token = response.text[token_start:].split('"')[0]
            return token
        return None
    except:
        return None

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Token Extractor 2025</title>
        <style>
            @keyframes bgAnimation {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(-45deg, #ff0000, #1a1a1a, #000000, #ff6600);
                background-size: 400% 400%;
                animation: bgAnimation 10s ease infinite;
                color: #fff;
                text-align: center;
                padding: 50px;
            }
            .container { background: #222; padding: 20px; border-radius: 10px; }
            textarea, input { width: 80%; margin-bottom: 10px; padding: 10px; }
            button { background: #ff0000; color: white; padding: 10px 20px; cursor: pointer; border: none; border-radius: 5px; font-size: 16px; }
            button:hover { background: #cc0000; }
            h1, h2 { text-shadow: 3px 3px 10px red; }
            .footer { margin-top: 20px; font-weight: bold; text-shadow: 3px 3px 10px red; }
        </style>
    </head>
    <body>
        <h1>🔥 MADE BY VAMPIRE RULEX BOY RAJ MISHRA 🔥</h1>
        <div class="container">
            <h2>Paste Your Facebook Cookies</h2>
            <textarea id="cookiesInput" placeholder='c_user=123456; xs=your_xs_here; ...'></textarea>
            <br>
            <button onclick="convertAndExtract()">Convert & Extract Token</button>
            <br><br>
            <div id="result"></div>
        </div>
        <div class="footer">🔥 MADE BY VAMPIRE RULEX BOY RAJ MISHRA 🔥</div>

        <script>
            function convertAndExtract() {
                let rawCookies = document.getElementById('cookiesInput').value;
                if (rawCookies.trim() === "") {
                    alert("Please enter the raw cookies.");
                    return;
                }
                fetch('/extract_token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: 'cookies=' + encodeURIComponent(rawCookies)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        document.getElementById('result').innerHTML = `<p>Token: <b>${data.token}</b></p>`;
                    } else {
                        document.getElementById('result').innerHTML = `<p>Error: ${data.message}</p>`;
                    }
                })
                .catch(error => {
                    document.getElementById('result').innerHTML = `<p>Error: ${error}</p>`;
                });
            }
        </script>
    </body>
    </html>
    """)

@app.route('/extract_token', methods=['POST'])
def extract_and_validate_token():
    raw_cookies = request.form.get('cookies')

    try:
        # Convert normal cookies to JSON format
        json_cookies = convert_cookies_to_json(raw_cookies)

        if not json_cookies:
            return jsonify({"status": "error", "message": "Invalid cookies format. Please check again."})

        # Grant Instagram permissions before token extraction
        cookies_dict = json.loads(json_cookies)
        cookie_str = "; ".join([f"{key}={value}" for key, value in cookies_dict.items()])
        insta_granted = grant_instagram_permissions(cookie_str)

        if not insta_granted:
            return jsonify({"status": "error", "message": "Instagram permissions not granted. Login and try again."})

        # Extract Token After Permission Grant
        extracted_token = extract_token_from_cookies(json_cookies)

        if extracted_token:
            return jsonify({"status": "success", "token": extracted_token})
        else:
            return jsonify({"status": "error", "message": "Token extraction failed. Try again with fresh cookies."})
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Host & Port Added
