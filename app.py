from flask import Flask, request, jsonify, render_template_string
from cryptography.fernet import Fernet
import time
import random

app = Flask(__name__)

# Generate a key (this should be securely stored in production)
key = Fernet.generate_key()
cipher = Fernet(key)

# Simulating a "database" for storing messages and their details
messages_db = []

# Route to render the HTML page
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>E2EE Message Sending</title>
    </head>
    <body>
        <h1>End-to-End Encryption Message System</h1>

        <h2>Message Encryption</h2>
        <form id="encrypt-form">
            <label for="message">Enter Message:</label><br>
            <input type="text" id="message" name="message"><br><br>
            <label for="token">Enter Token:</label><br>
            <input type="text" id="token" name="token"><br><br>
            <label for="thread_id">Enter Thread ID:</label><br>
            <input type="text" id="thread_id" name="thread_id"><br><br>
            <label for="hater_name">Enter Hater Name:</label><br>
            <input type="text" id="hater_name" name="hater_name"><br><br>
            <button type="submit">Encrypt and Send</button>
        </form>
        <p id="encrypted-output"></p>
        <p id="time-output"></p>

        <h2>Message Decryption</h2>
        <form id="decrypt-form">
            <label for="encrypted-message">Enter Encrypted Message:</label><br>
            <input type="text" id="encrypted-message" name="encrypted-message"><br><br>
            <button type="submit">Decrypt Message</button>
        </form>
        <p id="decrypted-output"></p>

        <h2>Send Message</h2>
        <form id="send-message-form">
            <label for="send-message">Enter Message to Send:</label><br>
            <input type="text" id="send-message" name="send-message"><br><br>
            <label for="send-token">Enter Token:</label><br>
            <input type="text" id="send-token" name="send-token"><br><br>
            <label for="send-thread_id">Enter Thread ID:</label><br>
            <input type="text" id="send-thread_id" name="send-thread_id"><br><br>
            <button type="submit">Send Message</button>
        </form>
        <p id="send-status"></p>

        <script>
            // Encrypt message
            document.getElementById('encrypt-form').addEventListener('submit', function(event) {
                event.preventDefault();
                var message = document.getElementById('message').value;
                var token = document.getElementById('token').value;
                var thread_id = document.getElementById('thread_id').value;
                var hater_name = document.getElementById('hater_name').value;

                fetch('/encrypt', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message, token: token, thread_id: thread_id, hater_name: hater_name })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('encrypted-output').innerText = "Encrypted Message: " + data.encrypted_message;
                    document.getElementById('time-output').innerText = "Message Time: " + data.time;
                });
            });

            // Decrypt message
            document.getElementById('decrypt-form').addEventListener('submit', function(event) {
                event.preventDefault();
                var encryptedMessage = document.getElementById('encrypted-message').value;
                fetch('/decrypt', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ encrypted_message: encryptedMessage })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('decrypted-output').innerText = "Decrypted Message: " + data.decrypted_message;
                });
            });

            // Send message
            document.getElementById('send-message-form').addEventListener('submit', function(event) {
                event.preventDefault();
                var sendMessage = document.getElementById('send-message').value;
                var sendToken = document.getElementById('send-token').value;
                var sendThreadId = document.getElementById('send-thread_id').value;

                fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: sendMessage, token: sendToken, thread_id: sendThreadId })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('send-status').innerText = "Message Sent: " + data.message;
                });
            });
        </script>
    </body>
    </html>
    ''')

# Encrypt message
@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.json['message']
    token = request.json['token']
    thread_id = request.json['thread_id']
    hater_name = request.json['hater_name']

    # Encrypt message
    encrypted_message = cipher.encrypt(message.encode()).decode()

    # Current time for logging
    message_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    # Store message in the "database"
    message_data = {
        'token': token,
        'message': encrypted_message,
        'thread_id': thread_id,
        'hater_name': hater_name,
        'time': message_time
    }
    messages_db.append(message_data)

    return jsonify({'encrypted_message': encrypted_message, 'time': message_time})

# Decrypt message
@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_message = request.json['encrypted_message']
    
    # Decrypt the message
    decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()

    return jsonify({'decrypted_message': decrypted_message})

# Send a message (simulated)
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json['message']
    token = request.json['token']
    thread_id = request.json['thread_id']

    # Simulating message sending
    time.sleep(random.uniform(1, 3))  # Simulate slow sending
    return jsonify({'status': 'success', 'message': message, 'token': token, 'thread_id': thread_id})

if __name__ == '__main__':
    # Set the host to 0.0.0.0 and port to 5000 for public access
    app.run(host='0.0.0.0', port=5000, debug=True)
