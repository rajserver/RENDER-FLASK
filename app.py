from flask import Flask, request, jsonify, render_template_string
import requests
import time
import random

app = Flask(__name__)

FB_SEND_URL = "https://www.facebook.com/messaging/send/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Mobile Safari/537.36"
}

def parse_cookies(raw_cookies):
    """Normal cookies ko JSON dict me convert karta hai"""
    cookies = {}
    for cookie in raw_cookies.split(";"):
        parts = cookie.strip().split("=", 1)
        if len(parts) == 2:
            cookies[parts[0]] = parts[1]
    return cookies

def send_message(uid, message, cookies):
    """Message send karne ka function"""
    if not cookies:
        return False

    msg_url = f"{FB_SEND_URL}?ids={uid}"
    data = {"message_body": message}
    
    response = requests.post(msg_url, headers=HEADERS, cookies=cookies, data=data)
    return response.status_code == 200

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🔥 Facebook Auto Messenger 🔥</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: black; color: white; }
            input, textarea, button { padding: 10px; margin: 10px; width: 80%; max-width: 400px; }
        </style>
    </head>
    <body>
        <h1>🔥 Facebook Auto Messenger 🔥</h1>
        <textarea id="cookies" placeholder="Paste Facebook Cookies Here"></textarea>
        <input type="text" id="uid" placeholder="Enter User ID">
        <input type="text" id="message" placeholder="Enter Message">
        <button onclick="sendMessage()">Send Message</button>
        <p id="status"></p>

        <script>
            function sendMessage() {
                const cookies = document.getElementById("cookies").value;
                const uid = document.getElementById("uid").value;
                const message = document.getElementById("message").value;

                if (!cookies || !uid || !message) {
                    document.getElementById("status").innerText = "❌ Please enter all details!";
                    return;
                }

                fetch("/send", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ cookies, uid, message })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("status").innerText = data.message;
                });
            }
        </script>
    </body>
    </html>
    """)

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    raw_cookies = data.get("cookies", "")
    uid = data.get("uid")
    message = data.get("message")

    if not raw_cookies or not uid or not message:
        return jsonify({"status": "error", "message": "Cookies, UID, aur Message required hai!"})

    cookies = parse_cookies(raw_cookies)
    success = send_message(uid, message, cookies)

    if success:
        return jsonify({"status": "success", "message": f"✅ Message sent to {uid}!"})
    else:
        return jsonify({"status": "error", "message": "❌ Failed to send message!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
