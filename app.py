from flask import Flask, request, render_template_string, jsonify
import json
import requests
import random
import time
import os
import threading
import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# To track the different processes (like loaders)
loaders_status = {}

# Function to simulate pinging server and checking uptime
def monitor_loader(loader_id):
    while loaders_status[loader_id]["running"]:
        loaders_status[loader_id]["uptime"] += 1  # Increment uptime
        time.sleep(60)  # Ping every 60 seconds
        # Simulate ping check (you can replace this with an actual server ping)
        response = requests.get("https://yourserver.com/ping")
        if response.status_code != 200:
            loaders_status[loader_id]["status"] = "Error"
        time.sleep(60)

def get_access_token(cookies=None, token=None, cookies_file=None):
    if cookies:
        access_token = extract_token_from_cookies(cookies)
        return access_token
    elif token:
        return token
    elif cookies_file:
        with open(cookies_file, 'r') as f:
            cookies_data = json.load(f)
        access_token = extract_token_from_cookies(cookies_data)
        return access_token
    else:
        return None

def send_comment(access_token, post_id, message):
    url = f"https://graph.facebook.com/v22.0/{post_id}/comments"
    payload = {"message": message, "access_token": access_token}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return {"status": "success", "message": "Comment sent successfully"}
    else:
        return {"status": "error", "message": "Failed to send comment", "details": response.json()}

def random_delay():
    delay = random.randint(10, 30)
    time.sleep(delay)

def retry_send_comment(access_token, post_id, message, retries=3):
    for _ in range(retries):
        result = send_comment(access_token, post_id, message)
        if result['status'] == 'success':
            return result
        random_delay()
    return {"status": "error", "message": "Failed to send after retries"}

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>POST SERVER BY RAJ MISHRA</title>
        <style>
            body {
                background: url('https://i.pinimg.com/originals/3b/2d/74/3b2d742fe607b2707be8f26d5e1d4655.gif') no-repeat center center fixed;
                background-size: cover;
                color: #fff;
                font-family: Arial, sans-serif;
                padding: 30px;
                margin: 0;
                animation: backgroundAnimation 30s infinite alternate;
            }

            @keyframes backgroundAnimation {
                0% { background-color: rgba(0, 0, 0, 0.7); }
                100% { background-color: rgba(0, 0, 0, 0.9); }
            }

            .container {
                max-width: 600px;
                margin: auto;
                background: rgba(0, 0, 0, 0.7);
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                animation: fadeIn 3s ease-in-out;
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }

            h2 {
                text-align: center;
            }

            input, textarea, button {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }

            button {
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }

            button:hover {
                background-color: #45a049;
            }

            footer {
                text-align: center;
                margin-top: 30px;
                font-size: 14px;
                color: #bbb;
            }

            .loader-info {
                color: #ddd;
                font-size: 12px;
                margin-top: 10px;
            }

        </style>
    </head>
    <body>
        <div class="container">
            <h2>POST SERVER BY RAJ MISHRA</h2>
            <form action="/comment" method="POST" enctype="multipart/form-data">
                <label for="haternames">Hater's Names (comma-separated)</label>
                <input type="text" id="haternames" name="haternames" required>
                
                <label for="post_id">Post ID</label>
                <input type="text" id="post_id" name="post_id" required>
                
                <label for="messages">Messages (comma-separated)</label>
                <textarea id="messages" name="messages" rows="4" required></textarea>
                
                <label for="last_names">Last Names (comma-separated)</label>
                <input type="text" id="last_names" name="last_names" required>
                
                <label for="tokens">Tokens (comma-separated)</label>
                <input type="text" id="tokens" name="tokens" required>
                
                <button type="submit">Send Comments</button>
            </form>

            <div class="loader-info">
                <p>Loader Status:</p>
                {% for loader, status in loaders_status.items() %}
                    <p>{{ loader }} - Uptime: {{ status["uptime"] }} mins, Status: {{ status["status"] }} 
                    <button onclick="stopLoader('{{ loader }}')">Stop</button></p>
                {% endfor %}
            </div>
        </div>

        <footer>
            DEVELOPED BY VAMPIRE RULEX BOY RAJ MISHRA
        </footer>
    </body>
    </html>
    """)

@app.route('/comment', methods=['POST'])
def comment():
    data = request.form
    haternames = data.get('haternames').split(',')
    post_id = data.get('post_id')
    messages = data.get('messages').split(',')
    last_names = data.get('last_names').split(',')
    tokens = data.get('tokens').split(',')
    
    # Loop through each set of input and send the comment
    for hatername, message, last_name, token in zip(haternames, messages, last_names, tokens):
        formatted_message = f"{hatername.strip()} {message.strip()} {last_name.strip()}"
        access_token = get_access_token(token=token)
        
        if not access_token:
            return jsonify({"status": "error", "message": "Invalid token provided"}), 400
        
        result = retry_send_comment(access_token, post_id, formatted_message)
        
        # Start a monitoring thread for this loader
        loader_id = f"loader_{len(loaders_status) + 1}"
        loaders_status[loader_id] = {
            "status": "Running",
            "uptime": 0,
            "running": True
        }
        
        # Start a background thread to monitor the loader
        threading.Thread(target=monitor_loader, args=(loader_id,)).start()

    return jsonify({"status": "success", "message": "Comments are being processed"})


# To stop a loader's monitoring
@app.route('/stop_loader', methods=['POST'])
def stop_loader():
    loader_id = request.form['loader_id']
    if loader_id in loaders_status:
        loaders_status[loader_id]["running"] = False
        return jsonify({"status": "success", "message": f"{loader_id} stopped"}), 200
    else:
        return jsonify({"status": "error", "message": "Loader not found"}), 404

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
