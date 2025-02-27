from flask import Flask, request, render_template_string
import random
import string
import hashlib
import requests

app = Flask(__name__)

# Free Proxy List (Fake IP ke liye)
PROXIES = [
    "http://45.79.58.206:8080",
    "http://188.166.17.5:3128",
    "http://103.253.208.112:3128"
]

# Fake IP Generator
def get_random_proxy():
    return random.choice(PROXIES)

def get_fake_ip():
    proxy = get_random_proxy()
    try:
        response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        ip = response.json().get("origin", "Unknown IP")
        return ip
    except:
        return "Proxy Failed"

# Facebook Accepted Emails Generate Karna
def generate_realistic_email():
    domains = ["@outlook.com", "@hotmail.com", "@gmail.com", "@yahoo.com", "@aol.com", "@protonmail.com"]
    first_names = ["raj", "vikas", "priya", "ravi", "anita", "amit", "rahul", "deepak"]
    last_names = ["sharma", "verma", "kumar", "yadav", "patel", "gupta", "singh", "joshi"]
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    number = random.randint(100, 999)  # Random Number for Realism
    email = f"{first}{last}{number}{random.choice(domains)}"
    return email

# Fixed 5-Digit Verification Code (Same for that Email Always)
def generate_verification_code(email):
    hashed = hashlib.md5(email.encode()).hexdigest()
    fixed_code = str(int(hashed[:5], 16) % 90000 + 10000)
    return fixed_code

@app.route("/", methods=["GET", "POST"])
def index():
    email = None
    verification_code = None
    fake_ip = "Not Generated"

    if request.method == "POST":
        email = generate_realistic_email()
        verification_code = generate_verification_code(email)
        fake_ip = get_fake_ip()

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FB Account Email Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: black;
                color: white;
                padding: 20px;
            }
            button {
                background-color: #ff0000;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                margin-top: 20px;
            }
            button:hover {
                background-color: #b30000;
            }
            .box {
                margin-top: 20px;
                padding: 15px;
                background: #222;
                display: inline-block;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            }
            .copy-btn {
                background-color: #007bff;
                color: white;
                padding: 5px 10px;
                border: none;
                cursor: pointer;
                font-size: 14px;
                margin-left: 10px;
            }
            .copy-btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>

        <h1>🔥 FB Account Email Generator 🔥</h1>
        <form method="POST">
            <button type="submit">Generate Facebook Email</button>
        </form>

        {% if email %}
        <div class='box'>
            <p><strong>Email:</strong> <span id='email'>{{ email }}</span> 
            <button class='copy-btn' onclick='copyText("email")'>Copy</button></p>
            
            <p><strong>Verification Code:</strong> <span id='code'>{{ verification_code }}</span> 
            <button class='copy-btn' onclick='copyText("code")'>Copy</button></p>

            <p><strong>Fake IP:</strong> {{ fake_ip }}</p>
        </div>
        {% endif %}

        <script>
            function copyText(id) {
                var text = document.getElementById(id).innerText;
                navigator.clipboard.writeText(text).then(function() {
                    alert("Copied: " + text);
                });
            }
        </script>

    </body>
    </html>
    """, email=email, verification_code=verification_code, fake_ip=fake_ip)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
