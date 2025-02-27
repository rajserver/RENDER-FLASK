from flask import Flask, request, render_template_string
import requests
import random
import time

app = Flask(__name__)

# Temporary Email API
EMAIL_API = "https://www.1secmail.com/api/v1/"
EMAIL_DOMAIN = "1secmail.com"

# Generate Random Email
def generate_email():
    username = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=10))
    email = f"{username}@{EMAIL_DOMAIN}"
    return email, username

# Fetch OTP From Email Inbox
def fetch_otp(username):
    time.sleep(5)  # Wait for OTP to arrive
    try:
        inbox = requests.get(f"{EMAIL_API}?action=getMessages&login={username}&domain={EMAIL_DOMAIN}").json()
        if inbox:
            msg_id = inbox[0]['id']
            msg = requests.get(f"{EMAIL_API}?action=readMessage&login={username}&domain={EMAIL_DOMAIN}&id={msg_id}").json()
            otp = ''.join(filter(str.isdigit, msg['textBody']))
            return otp
    except:
        pass
    return "Waiting for OTP..."

@app.route("/", methods=["GET", "POST"])
def index():
    email = otp = None
    if request.method == "POST":
        email, username = generate_email()
        otp = fetch_otp(username)

    return render_template_string("""
    <html>
    <head>
        <title>FB Auto-Verified Email</title>
        <style>
            body { background: black; color: white; text-align: center; }
            .box { padding: 10px; border: 1px solid red; display: inline-block; }
            button { background: red; color: white; padding: 5px 10px; border: none; }
        </style>
    </head>
    <body>
        <h1>🔥 FB Auto-Verified Email 🔥</h1>
        <form method="POST">
            <button type="submit">Generate Email</button>
        </form>
        {% if email %}
        <div class="box">
            <p>Email: <b>{{ email }}</b></p>
            <p>OTP: <b>{{ otp }}</b></p>
        </div>
        {% endif %}
    </body>
    </html>
    """, email=email, otp=otp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
