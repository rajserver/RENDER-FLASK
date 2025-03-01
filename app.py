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

# Fetch OTP From Email Inbox (Auto-Retry)
def fetch_otp(username):
    for _ in range(12):  # 12 retries (5 sec each = 1 min)
        try:
            inbox = requests.get(f"{EMAIL_API}?action=getMessages&login={username}&domain={EMAIL_DOMAIN}").json()
            if inbox:
                msg_id = inbox[0]['id']
                msg = requests.get(f"{EMAIL_API}?action=readMessage&login={username}&domain={EMAIL_DOMAIN}&id={msg_id}").json()
                otp = ''.join(filter(str.isdigit, msg['textBody']))
                return otp
        except:
            pass
        time.sleep(5)  # Wait for 5 sec before retrying
    return "OTP not received, try again!"

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
            .copy-btn { background: blue; color: white; padding: 3px 7px; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>🔥 FB Auto-Verified Email 🔥</h1>
        <form method="POST">
            <button type="submit">Generate Email</button>
        </form>
        {% if email %}
        <div class="box">
            <p>Email: <b id="email">{{ email }}</b> <button class="copy-btn" onclick="copyText('email')">Copy</button></p>
            <p>OTP: <b id="otp">{{ otp }}</b> <button class="copy-btn" onclick="copyText('otp')">Copy</button></p>
        </div>
        {% endif %}
        <script>
            function copyText(id) {
                var text = document.getElementById(id).innerText;
                navigator.clipboard.writeText(text);
                alert("Copied: " + text);
            }
        </script>
    </body>
    </html>
    """, email=email, otp=otp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
