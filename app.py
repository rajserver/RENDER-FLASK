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
        access_token = extract_token_from_cookies(cookies)  # Implement your extraction method
        return access_token
    elif token:
        return token  # Direct token use
    elif cookies_file:
        with open(cookies_file, 'r') as f:
            cookies_data = json.load(f)
        access_token = extract_token_from_cookies(cookies_data)  # Implement token extraction logic
        return access_token
    else:
        return None

# Facebook Graph API to send a comment
def send_comment(access_token, post_id, message):
    url = f"https://graph.facebook.com/v22.0/{post_id}/comments"
    payload = {
        "message": message,
        "access_token": access_token
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return {"status": "success", "message": "Comment sent successfully"}
    else:
        return {"status": "error", "message": "Failed to send comment", "details": response.json()}

# Random delay to avoid bot detection
def random_delay():
    delay = random.randint(10, 30)  # Random delay between 10-30 seconds
    time.sleep(delay)

# Retry sending comment if it fails
def retry_send_comment(access_token, post_id, message, retries=3):
    for _ in range(retries):
        result = send_comment(access_token, post_id, message)
        if result['status'] == 'success':
            return result
        random_delay()
    return {"status": "error", "message": "Failed to send after retries"}

# Home route
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
                <label for="hatername">Hater's Name (Multiple Names separated by commas)</label>
                <input type="text" id="hatername" name="hatername" required>
                
                <label for="post_id">Post ID</label>
                <input type="text" id="post_id" name="post_id" required>
                
                <label for="message">Message (Multiple Messages separated by commas)</label>
                <textarea id="message" name="message" rows="4" required></textarea>
                
                <label for="last_name">Last Name (Multiple Last Names separated by commas)</label>
                <input type="text" id="last_name" name="last_name" required>
                
                <label for="token">Tokens (Multiple Tokens separated by commas)</label>
                <input type="text" id="token" name="token" placeholder="Enter your Facebook tokens">
                
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
    haternames = data.get('hatername').split(',')
    post_id = data.get('post_id')
    last_names = data.get('last_name').split(',')
    messages = data.get('message').split(',')
    
    cookies_file = request.files.get('cookies_file')
    tokens = data.get('token').split(',')
    
    if not post_id or not messages or not haternames or not last_names:
        return jsonify({"status": "error", "message": "Post ID, message, hatername, and last name are required"}), 400
    
    access_tokens = []
    for token in tokens:
        access_token = get_access_token(cookies_file=cookies_file, token=token)
        if access_token:
            access_tokens.append(access_token)
    
    if not access_tokens:
        return jsonify({"status": "error", "message": "No valid tokens or cookies provided"}), 400
    
    # Send comment for each combination of hatername, message, last name, and token
    for hatername in haternames:
        for message in messages:
            for last_name in last_names:
                formatted_message = f"{hatername.strip()} {message.strip()} {last_name.strip()}"
                for access_token in access_tokens:
                    result = retry_send_comment(access_token, post_id, formatted_message)
                    random_delay()

    return jsonify({"status": "success", "message": "Comments sent successfully"})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
