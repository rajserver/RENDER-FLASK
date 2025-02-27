from flask import Flask, request
import random
import string
import hashlib
import requests  # Proxy ke liye

app = Flask(__name__)

# Free Proxy List (Agar koi premium proxy hai to use kar sakte ho)
PROXIES = [
    "http://45.79.58.206:8080",
    "http://188.166.17.5:3128",
    "http://103.253.208.112:3128"
]

# Random Proxy Select Karega
def get_random_proxy():
    return random.choice(PROXIES)

# Random Email Generate Karna
def generate_random_email():
    domains = ["@tempmail.net", "@mailinator.com", "@yopmail.com"]
    random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = random_name + random.choice(domains)
    return email

# Fixed Verification Code Generate Karna
def generate_verification_code(email):
    hashed = hashlib.md5(email.encode()).hexdigest()
    return hashed[:6]

# Proxy ke through request bhejna (Fake IP ke liye)
def get_fake_ip():
    proxy = get_random_proxy()
    try:
        response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        ip = response.json().get("origin", "Unknown IP")
        return ip
    except:
        return "Proxy Failed"

# Main Flask Route
@app.route("/", methods=["GET", "POST"])
def index():
    email = None
    verification_code = None
    fake_ip = "Not Generated"

    if request.method == "POST":
        email = generate_random_email()
        verification_code = generate_verification_code(email)
        fake_ip = get_fake_ip()  # Proxy ke through naya IP

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Email Generator</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: black;
                color: white;
                padding: 20px;
            }}
            button {{
                background-color: #ff0000;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                margin-top: 20px;
            }}
            button:hover {{
                background-color: #b30000;
            }}
            .box {{
                margin-top: 20px;
                padding: 15px;
                background: #222;
                display: inline-block;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            }}
        </style>
    </head>
    <body>

        <h1>🔥 Facebook Email Generator 🔥</h1>
        <form method="POST">
            <button type="submit">Generate Facebook Email</button>
        </form>

        {"<div class='box'><p><strong>Email:</strong> " + email + "</p><p><strong>Verification Code:</strong> " + verification_code + "</p><p><strong>Fake IP:</strong> " + fake_ip + "</p></div>" if email else ""}
    
    </body>
    </html>
    """

# Flask Run on Port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
