from flask import Flask, render_template_string, request
from twilio.rest import Client
import random
import time
import threading
import os
import logging

app = Flask(__name__)

# File upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'csv'}

# Set up logging
logging.basicConfig(level=logging.INFO)

# Dummy Twilio SID and Auth Token (Replace with actual credentials manually)
account_sid = os.getenv('TWILIO_ACCOUNT_SID')  # Environment variable se Twilio SID
auth_token = os.getenv('TWILIO_AUTH_TOKEN')  # Environment variable se Twilio Auth Token
twilio_number = os.getenv('TWILIO_NUMBER')  # WhatsApp sandbox number, set from environment

client = Client(account_sid, auth_token)

# Stop flags for controlling the message sending for specific contact or group
stop_contact_flag = None
stop_group_flag = None

# Function to randomize message content from the specific file (File.txt)
def randomize_message():
    try:
        # Check if the file exists
        message_file = os.path.join(app.config['UPLOAD_FOLDER'], 'File.txt')
        if not os.path.exists(message_file):
            logging.error("File.txt not found!")
            return "Error: File.txt not found!"  # Default error message
        
        with open(message_file, 'r') as file:
            messages = file.readlines()
        return random.choice(messages).strip()  # Randomly choose one message
    except Exception as e:
        logging.error(f"Error reading message file: {e}")
        return "Hello, this is a test message."  # Default message if file read fails

# Function to send a message with random delay
def send_message(to_number, message, sender_number):
    global stop_contact_flag, stop_group_flag
    # Add a random delay before sending each message
    delay = random.uniform(3, 5)  # Random delay between 3 and 5 seconds
    time.sleep(delay)

    # Stop the sending process if stop flag for contact or group is set
    if stop_contact_flag == to_number:
        logging.info(f"Message sending stopped for contact {to_number}.")
        return

    if stop_group_flag == to_number:
        logging.info(f"Message sending stopped for group {to_number}.")
        return

    # Send message via Twilio
    client.messages.create(
        body=message,
        from_=f'whatsapp:{sender_number}',
        to=f'whatsapp:{to_number}'
    )
    logging.info(f"Message sent from {sender_number} to {to_number} with delay: {delay:.2f} seconds")

# Function to generate token automatically (This is just a placeholder for actual logic)
def generate_twilio_token(user_number):
    # Normally, Twilio doesn't generate tokens like this.
    # You would need to integrate OAuth or use Twilio's API with your SID and Auth Token
    logging.info(f"Generating Twilio token for {user_number}...")
    # Placeholder logic: Replace with real logic or manual step
    return account_sid, auth_token, twilio_number

# Route for the homepage and form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    global stop_contact_flag, stop_group_flag

    if request.method == 'POST':
        if request.form.get('action') == 'stop_contact':
            stop_contact_flag = request.form.get('contact_number')  # Stop sending messages to specific contact
            stop_group_flag = None  # Clear group flag if contact stop is selected
            logging.info(f"Stop message sending for contact: {stop_contact_flag}")
            return render_template_string(html_template, message=f"Message sending stopped for contact {stop_contact_flag}!")

        elif request.form.get('action') == 'stop_group':
            stop_group_flag = request.form.get('group_uid')  # Stop sending messages to specific group
            stop_contact_flag = None  # Clear contact flag if group stop is selected
            logging.info(f"Stop message sending for group: {stop_group_flag}")
            return render_template_string(html_template, message=f"Message sending stopped for group {stop_group_flag}!")

        # Reset the stop flags when starting to send messages
        stop_contact_flag = None
        stop_group_flag = None
        
        user_number = request.form.get('sender_number')
        
        # Generate Twilio credentials (fake logic here, please replace with actual token generation mechanism)
        account_sid, auth_token, twilio_number = generate_twilio_token(user_number)

        # Save the generated credentials to be used later
        # In production, you should store these in a safe place (e.g., a database or secure vault)
        
        recipients = request.form.get('recipients').split(',')
        message_limit = int(request.form.get('message_limit'))
        message_interval = int(request.form.get('message_interval')) * 60  # Convert minutes to seconds
        sender_number = user_number.strip()

        # Function to send messages
        def send_messages():
            sent_count = 0
            message_status = {}  # Dictionary to track sent messages per recipient
            
            for recipient in recipients:
                if recipient not in message_status:
                    message_status[recipient] = 0  # Initialize message count for recipient

                while sent_count < message_limit:
                    # Stop the sending process if stop flag is set
                    if stop_contact_flag == recipient or stop_group_flag == recipient:
                        logging.info(f"Message sending stopped for {recipient}.")
                        break

                    message = randomize_message()  # Randomize the message content
                    send_message(recipient.strip(), message, sender_number)
                    sent_count += 1
                    message_status[recipient] += 1  # Increment the message count for the recipient

                    # Check if the message limit is reached
                    if sent_count >= message_limit:
                        logging.info("Message limit reached.")
                        break

                    # Wait for the set interval before sending next message
                    time.sleep(message_interval)

            # Check if limit was exceeded for any recipient
            for recipient, count in message_status.items():
                if count >= 5:
                    logging.error(f"Failure: Unable to send more messages to {recipient}, limit exceeded.")

        # Start sending messages in a separate thread
        threading.Thread(target=send_messages).start()

        return render_template_string(html_template, message="Messages are being sent!")

    return render_template_string(html_template, message=None)

# Helper function to check if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# HTML Template
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Message Sender - Flask</title>
</head>
<body style="background-color:#f0f0f0; font-family: Arial, sans-serif; padding: 20px;">
    <h1>Message Sender by Raj Mishra</h1>
    <form method="POST">
        <h3>Stop Message Sending</h3>
        <label for="contact_number">Enter Contact Number to Stop:</label>
        <input type="text" id="contact_number" name="contact_number" placeholder="Enter contact number">
        <button type="submit" name="action" value="stop_contact">Stop for Contact</button>
    </form>

    <form method="POST">
        <label for="group_uid">Enter Group UID to Stop:</label>
        <input type="text" id="group_uid" name="group_uid" placeholder="Enter group UID">
        <button type="submit" name="action" value="stop_group">Stop for Group</button>
    </form>

    <h3>Send Messages</h3>
    <form method="POST">
        <label for="sender_number">Enter Your Number (WhatsApp):</label>
        <input type="text" id="sender_number" name="sender_number" placeholder="e.g. +1234567890" required><br><br>

        <label for="recipients">Enter Recipients (comma separated):</label>
        <input type="text" id="recipients" name="recipients" placeholder="e.g. +1234567890,+0987654321" required><br><br>

        <label for="message_limit">Message Limit:</label>
        <input type="number" id="message_limit" name="message_limit" placeholder="e.g. 10" required><br><br>

        <label for="message_interval">Message Interval (minutes):</label>
        <input type="number" id="message_interval" name="message_interval" placeholder="e.g. 2" required><br><br>

        <button type="submit">Start Sending Messages</button>
    </form>

    <p>{{ message }}</p>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Running on all IPs of the local machine
