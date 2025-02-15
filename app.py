from flask import Flask, request, render_template_string, jsonify
import json
import requests
import random
import time
import os

app = Flask(__name__)

# Folder for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to get Facebook access token from cookies or token directly
def get_access_token(cookies=None, token=None, cookies_file=None):
    if cookies:
        # Cookies se token extract karna (apne method ke according implement karein)
        access_token = extract_token_from_cookies(cookies)  # Yahan apna method use karen
        return access_token
    elif token:
        return token  # Direct token ka use
    elif cookies_file:
        # Cookies file se token extract karna
        with open(cookies_file, 'r') as f:
            cookies_data = json.load(f)
        access_token = extract_token_from_cookies(cookies_data)  # Token extraction logic implement karen
        return access_token
    else:
        return None

# Facebook Graph API ke through comment send karna
def send_comment(access_token, post_id, message):
    url = f"https://graph.facebook.com/v22.0/{post_id}/comments"
    payload = {
        "message": message,
        "access_token": access_token
    }

    # Post request to send comment
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return {"status": "success", "message": "Comment sent successfully"}
    else:
        return {"status": "error", "message": "Failed to send comment", "details": response.json()}

# Random delay function to avoid bot detection
def random_delay():
    delay = random.randint(10, 30)  # 10-30 second ke beech random delay
    time.sleep(delay)

# Retry logic agar comment send nahi hota
def retry_send_comment(access_token, post_id, message, retries=3):
    for _ in range(retries):
        result = send_comment(access_token, post_id, message)
        if result['status'] == 'success':
            return result
        random_delay()
    return {"status": "error", "message": "Failed to send after retries"}

# Home route (web page)
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
                background: url('https://images.unsplash.com/photo-1494448454025-87a5a142bf1e') no-repeat center center fixed;
                background-size: cover;
                color: #fff;
                font-family: Arial, sans-serif;
                padding: 30px;
                margin: 0;
            }
            .container {
                max-width: 600px;
                margin: auto;
                background: rgba(0, 0, 0, 0.5);
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            }
            h2 {
                text-align: center;
                color: #fff;
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
        </style>
    </head>
    <body>
        <div class="container">
            <h2>POST SERVER BY RAJ MISHRA</h2>
            <form action="/comment" method="POST" enctype="multipart/form-data">
                <label for="hatername">Hater's Name</label>
                <input type="text" id="hatername" name="hatername" required>
                
                <label for="post_id">Post ID</label>
                <input type="text" id="post_id" name="post_id" required>
                
                <label for="message">Message</label>
                <textarea id="message" name="message" rows="4" required></textarea>
                
                <label for="last_name">Last Name</label>
                <input type="text" id="last_name" name="last_name" required>
                
                <label for="token">Token</label>
                <input type="text" id="token" name="token" placeholder="Enter your Facebook token">
                
                <label for="cookies_file">Or Upload Cookies File</label>
                <input type="file" id="cookies_file" name="cookies_file" accept=".json">
                
                <button type="submit">Send Comment</button>
            </form>
        </div>
        <footer>
            DEVELOPED BY VAMPIRE RULEX BOY RAJ MISHRA
        </footer>
    </body>
    </html>
    """)

# Route to handle comment submission
@app.route('/comment', methods=['POST'])
def comment():
    data = request.form
    hatername = data.get('hatername')
    post_id = data.get('post_id')
    last_name = data.get('last_name')
    message = data.get('message')
    
    # File handling for token or cookies
    cookies_file = request.files.get('cookies_file')  # Expecting a file upload for cookies (JSON)
    token = data.get('token')  # Token ko direct pass kiya jaa sakta hai
    
    if not post_id or not message or not hatername or not last_name:
        return jsonify({"status": "error", "message": "Post ID, message, hatername, and last name are required"}), 400
    
    # Format message: hatername, message, last name
    formatted_message = f"{hatername} {message} {last_name}"
    
    # Get the access token from cookies file or token directly
    access_token = get_access_token(cookies_file=cookies_file, token=token)
    
    if not access_token:
        return jsonify({"status": "error", "message": "No valid token or cookies provided"}), 400
    
    # Send comment with retry logic
    result = retry_send_comment(access_token, post_id, formatted_message)
    
    return jsonify(result)

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
