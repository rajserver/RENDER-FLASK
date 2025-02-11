from flask import Flask, request, render_template_string, redirect
import requests
import random
import string
import time
from threading import Thread, Event
import os

app = Flask(__name__)

# Facebook OAuth URLs with permissions
FB_APP_ID = 'YOUR_APP_ID'  # Replace with your Facebook App ID
FB_APP_SECRET = 'YOUR_APP_SECRET'  # Replace with your Facebook App Secret
FB_OAUTH_URL = f"https://www.facebook.com/v15.0/dialog/oauth?client_id={FB_APP_ID}&redirect_uri=https://your_server_url.com/fb-callback&scope=public_profile,email,pages_show_list,instagram_basic,instagram_content_publish,manage_pages,read_page_mailboxes,pages_manage_metadata,pages_manage_posts"
FB_ACCESS_TOKEN_URL = "https://graph.facebook.com/v15.0/oauth/access_token"
FB_GRAPH_API_URL = "https://graph.facebook.com/v15.0/me"

# Function to exchange short-lived token for long-lived token
def get_long_lived_token(short_lived_token):
    url = f"{FB_ACCESS_TOKEN_URL}?grant_type=fb_exchange_token&client_id={FB_APP_ID}&client_secret={FB_APP_SECRET}&fb_exchange_token={short_lived_token}"
    response = requests.get(url)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        raise Exception("Failed to refresh the token.")

# Function to check if the token is valid (check expiry)
def check_token_validity(token):
    url = f"{FB_GRAPH_API_URL}?access_token={token}"
    response = requests.get(url)
    if response.status_code == 200:
        return True  # Token is valid
    else:
        return False  # Token has expired or is invalid

# Threading to send multiple messages
stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/')
def index():
    # Render a template with the Facebook OAuth URL
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VAMPIRE RULEX BOY RAJ MISHRA</title>
  <style>
      body { background-color: black; color: white; font-family: 'Courier New', Courier, monospace; }
      h1 { color: red; }
  </style>
</head>
<body>
  <h1>Login with Facebook</h1>
  <a href="{{ oauth_url }}" style="color: yellow; font-size: 20px;">Login with Facebook</a>
</body>
</html>
''', oauth_url=FB_OAUTH_URL)

@app.route('/fb-callback')
def fb_callback():
    # Handle the Facebook OAuth callback to extract the token
    code = request.args.get('code')

    if code:
        # Exchange code for access token
        url = f"{FB_ACCESS_TOKEN_URL}?client_id={FB_APP_ID}&redirect_uri=https://your_server_url.com/fb-callback&client_secret={FB_APP_SECRET}&code={code}"
        response = requests.get(url)
        data = response.json()
        if 'access_token' in data:
            access_token = data['access_token']
            long_lived_token = get_long_lived_token(access_token)  # Convert to long-lived token
            return f"Access Token: {long_lived_token}"
        else:
            return "Error: Unable to retrieve access token"
    else:
        return "Error: Missing code in callback"

@app.route('/validate-token', methods=['POST'])
def validate_token():
    token = request.form.get('token')

    if check_token_validity(token):
        return f"Token is valid: {token}"
    else:
        return f"Token is invalid: {token}"

@app.route('/send-message', methods=['POST'])
def send_message():
    token = request.form.get('access_token')
    thread_id = request.form.get('thread_id')
    message = request.form.get('message')

    # Validate token before sending the message
    if not check_token_validity(token):
        return "Error: Invalid Token"

    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
    parameters = {'access_token': token, 'message': message}
    response = requests.post(api_url, data=parameters)
    
    if response.status_code == 200:
        return f"Message Sent Successfully: {message}"
    else:
        return f"Error: Failed to send message. {response.text}"

@app.route('/send-bulk-message', methods=['POST'])
def send_bulk_message():
    token_option = request.form.get('tokenOption')

    if token_option == 'single':
        access_tokens = [request.form.get('singleToken')]
    else:
        token_file = request.files['tokenFile']
        access_tokens = token_file.read().decode().strip().splitlines()

    thread_id = request.form.get('threadId')
    mn = request.form.get('kidx')
    time_interval = int(request.form.get('time'))

    txt_file = request.files['txtFile']
    messages = txt_file.read().decode().splitlines()

    task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    stop_events[task_id] = Event()
    thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
    threads[task_id] = thread
    thread.start()

    return f'Task started with ID: {task_id}'

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return "Task ID not found."

if __name__ == '__main__':
    # Set your port and host for deployment, use '0.0.0.0' for external access
    app.run(host='0.0.0.0', port=5000, debug=True)
