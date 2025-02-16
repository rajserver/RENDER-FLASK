from flask import Flask, request, jsonify
import requests
import json
import time
import random

app = Flask(__name__)

FB_SEND_URL = "https://www.facebook.com/messaging/send/"
FB_E2EE_THREAD_URL = "https://www.facebook.com/api/graphql/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Mobile Safari/537.36"
}

COOKIES_FILE = "fb_cookies.json"

def load_cookies():
    try:
        with open(COOKIES_FILE, "r") as file:
            cookies = json.load(file)
        return cookies
    except:
        return None

def get_e2ee_thread_id(uid, cookies):
    data = {
        "fb_api_req_friendly_name": "MessengerThreadQuery",
        "variables": json.dumps({"id": uid}),
        "doc_id": "1234567890"
    }
    response = requests.post(FB_E2EE_THREAD_URL, headers=HEADERS, cookies=cookies, data=data)
    try:
        thread_id = response.json()["data"]["message_thread"]["thread_key"]
        return thread_id
    except:
        return None

def send_message(uid, message, cookies, message_type, e2ee_thread_id=None):
    if not cookies:
        return False

    if message_type == "e2ee":
        if not e2ee_thread_id:
            return False
        msg_url = f"{FB_SEND_URL}?thread_fbid={e2ee_thread_id}"
    else:
        msg_url = f"{FB_SEND_URL}?ids={uid}"

    data = {"message_body": message}
    response = requests.post(msg_url, headers=HEADERS, cookies=cookies, data=data)

    return response.status_code == 200

def auto_sender(uid, message, message_type, e2ee_thread_id):
    cookies = load_cookies()
    if not cookies:
        return {"status": "error", "message": "Cookies file invalid hai!"}

    start_time = time.time()
    while True:
        success = send_message(uid, message, cookies, message_type, e2ee_thread_id)
        
        if not success:
            time.sleep(2)
            continue

        sleep_time = random.randint(30, 90)
        elapsed_time = time.time() - start_time
        if elapsed_time + sleep_time > 600:
            sleep_time = 600 - elapsed_time
        
        time.sleep(sleep_time)
        start_time = time.time()

        return {"status": "success", "message": f"Message sent to {uid}"}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Auto Messenger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: black;
            color: white;
        }
        input, select, button {
            padding: 10px;
            margin: 10px;
            display: block;
            width: 80%;
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
</head>
<body>
    <h1>🔥 Facebook Auto Messenger 🔥</h1>
    <select id="message_type">
        <option value="inbox">Inbox Message</option>
        <option value="group">Group Message</option>
        <option value="e2ee">E2EE Encrypted Message</option>
    </select>
    <input type="text" id="uid" placeholder="Enter Group ID / Inbox Profile URL">
    <input type="text" id="e2ee_thread_id" placeholder="E2EE Thread ID (Only if required)">
    <input type="text" id="hatersname" placeholder="Enter Haters Name (Optional)">
    <input type="text" id="message" placeholder="Enter Message">
    <button onclick="sendMessage()">Send Message</button>
    <p id="status"></p>

    <script>
        function sendMessage() {
            const uid = document.getElementById("uid").value;
            const message = document.getElementById("message").value;
            const e2ee_thread_id = document.getElementById("e2ee_thread_id").value;
            const message_type = document.getElementById("message_type").value;
            const hatersname = document.getElementById("hatersname").value;

            if (!uid || !message) {
                document.getElementById("status").innerText = "❌ Please enter UID & Message!";
                return;
            }

            fetch("/send", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ uid, message, message_type, e2ee_thread_id, hatersname })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("status").innerText = data.message;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    uid = data.get("uid")
    message = data.get("message")
    message_type = data.get("message_type")
    e2ee_thread_id = data.get("e2ee_thread_id", None)
    hatersname = data.get("hatersname", "")

    if not uid or not message:
        return jsonify({"status": "error", "message": "UID aur Message required hai!"})

    if hatersname:
        message = f"@{hatersname} {message}"

    result = auto_sender(uid, message, message_type, e2ee_thread_id)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
