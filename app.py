from flask import Flask, request, render_template_string
import random
import string
import os

app = Flask(__name__)

# Pre-defined verification codes (Fixed for Each Email)
VERIFICATION_CODES = {}

# Facebook Accepted Emails Generate Karna
def generate_realistic_email():
    domains = ["@outlook.com", "@hotmail.com", "@gmail.com", "@yahoo.com", "@aol.com", "@protonmail.com"]
    first_names = ["raj", "vikas", "priya", "ravi", "anita", "amit", "rahul", "deepak"]
    last_names = ["sharma", "verma", "kumar", "yadav", "patel", "gupta", "singh", "joshi"]
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    number = random.randint(100, 999)  # Random Number for Realism
    email = f"{first}{last}{number}{random.choice(domains)}"
    
    # Agar pehle se exist karta hai to wahi code milega
    if email in VERIFICATION_CODES:
        verification_code = VERIFICATION_CODES[email]
    else:
        verification_code = str(random.randint(10000, 99999))  # Fixed 5-digit Code for this Email
        VERIFICATION_CODES[email] = verification_code  # Store the Fixed Code

    return email, verification_code

@app.route("/", methods=["GET", "POST"])
def index():
    email = None
    verification_code = None

    if request.method == "POST":
        email, verification_code = generate_realistic_email()

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
    """, email=email, verification_code=verification_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
