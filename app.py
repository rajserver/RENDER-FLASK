from Crypto.Cipher import AES
import base64
import hashlib
import json
import time
from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

# Function to pad the message to be a multiple of 16 bytes (AES block size)
def pad_message(message):
    return message + (16 - len(message) % 16) * ' '

# Function to encrypt the message using AES (ECB mode)
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_message = pad_message(message)
    encrypted = cipher.encrypt(padded_message.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# Function to send the encrypted message using cookies for authentication
def send_encrypted_message(cookie, thread_id, encrypted_message):
    url = f'https://www.messenger.com/t/{thread_id}'

    headers = {
        'Content-Type': 'application/json',
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }

    payload = {
        'message': encrypted_message  # The encrypted message to send
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return "Message sent successfully!"
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to read cookies from JSON
def read_cookies_from_json(cookie_json):
    try:
        with open(cookie_json, 'r') as file:
            cookies = json.load(file)
        return cookies
    except Exception as e:
        return str(e)

# Home route that shows the form to the user
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get data from the form
        message = request.form.get('message')
        thread_id = request.form.get('thread_id')
        cookie_json = request.form.get('cookie_json')
        e2ee_key = hashlib.sha256("secret_key_for_encryption".encode()).digest()

        # Read cookies in JSON format
        cookies = read_cookies_from_json(cookie_json)
        if isinstance(cookies, str):  # Error reading cookies
            return jsonify({'error': cookies})

        cookie = cookies.get('cookie')  # Make sure cookie is in the JSON file

        # Encrypt the message
        encrypted_message = encrypt_message(message, e2ee_key)

        # Send the encrypted message
        result = send_encrypted_message(cookie, thread_id, encrypted_message)
        return render_template_string(HTML_TEMPLATE, result=result)

    return render_template_string(HTML_TEMPLATE)

# Define the HTML Template directly in the script
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E2EE Message Sender</title>
</head>
<body>
    <h1>Send E2EE Encrypted Message</h1>

    <form method="POST" action="/">
        <label for="message">Message:</label><br>
        <input type="text" id="message" name="message" required><br><br>

        <label for="thread_id">Thread ID:</label><br>
        <input type="text" id="thread_id" name="thread_id" required><br><br>

        <label for="cookie_json">Path to cookie JSON:</label><br>
        <input type="text" id="cookie_json" name="cookie_json" required><br><br>

        <button type="submit">Send Message</button>
    </form>

    {% if result %}
    <h2>{{ result }}</h2>
    {% endif %}

    <h3>Additional Features</h3>
    <!-- Implement time and stop functionality here -->
    <button onclick="stopProcess()">Stop</button>

    <script>
        function stopProcess() {
            alert("Process stopped!");  // You can expand this function based on your needs.
        }
    </script>
</body>
</html>
'''

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
