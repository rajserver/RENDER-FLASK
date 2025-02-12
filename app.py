import requests
import json
import base64
from datetime import datetime
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Function to extract the token from cookies (in JSON format)
def extract_token_from_cookies(cookie_str):
    cookies = json.loads(cookie_str)  # Convert JSON string to dictionary
    return cookies.get('access_token')  # Get the access_token from the cookies

# Function to encrypt the message using the E2EE encryption key
def encrypt_message(message, encryption_key):
    key_bytes = base64.b64decode(encryption_key)  # Convert the encryption key to bytes
    # Simple encryption approach, just for demonstration (real E2EE needs more complex cryptographic operations)
    encrypted_message = base64.b64encode(message.encode('utf-8'))  # Basic encryption (in practice, use E2EE libraries)
    return encrypted_message

# Function to send the encrypted message
def send_e2ee_message(token, thread_id, encrypted_message, encryption_key, hatersname, time_to_send):
    url = f"https://www.facebook.com/messages/e2ee/t/{thread_id}"  # E2EE message URL
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    data = {
        'message': encrypted_message.decode('utf-8'),
        'thread_id': thread_id,
        'encryption_key': encryption_key,
        'hatersname': hatersname,
        'time_to_send': time_to_send,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# HTML Template with embedded Flask routes
@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Send E2EE Message</title>
    </head>
    <body>
        <h1>Send E2EE Message</h1>
        <form action="/send" method="POST" enctype="multipart/form-data">
            <label for="token">Access Token:</label><br>
            <input type="text" id="token" name="token" required><br><br>

            <label for="thread_id">Thread ID:</label><br>
            <input type="text" id="thread_id" name="thread_id" required><br><br>

            <label for="encryption_key">Encryption Key:</label><br>
            <input type="text" id="encryption_key" name="encryption_key" required><br><br>

            <label for="hatersname">Haters Name:</label><br>
            <input type="text" id="hatersname" name="hatersname" required><br><br>

            <label for="time_to_send">Time to Send:</label><br>
            <input type="datetime-local" id="time_to_send" name="time_to_send" required><br><br>

            <label for="message">Message:</label><br>
            <textarea id="message" name="message" required></textarea><br><br>

            <label for="message_file">Message File (Optional):</label><br>
            <input type="file" id="message_file" name="message_file"><br><br>

            <button type="submit">Send Message</button>
        </form>
    </body>
    </html>
    ''')

@app.route('/send', methods=['POST'])
def send_message():
    token = request.form['token']
    thread_id = request.form['thread_id']
    encryption_key = request.form['encryption_key']
    hatersname = request.form['hatersname']
    time_to_send = request.form['time_to_send']
    message = request.form['message']
    message_file = request.files['message_file']  # File upload for messages

    # Encrypt the message
    encrypted_message = encrypt_message(message, encryption_key)

    # Optionally save the message file
    if message_file:
        message_file.save(f"messages/{message_file.filename}")
        print(f"Message file {message_file.filename} saved.")

    # Send the encrypted message
    send_e2ee_message(token, thread_id, encrypted_message, encryption_key, hatersname, time_to_send)

    return "Message Sent Successfully!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
