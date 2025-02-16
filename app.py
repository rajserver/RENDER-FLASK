from flask import Flask, request, jsonify, render_template_string, redirect
import requests

app = Flask(__name__)

# Replace with your actual Facebook App ID and Secret
FACEBOOK_APP_ID = 'your_app_id'
FACEBOOK_APP_SECRET = 'your_app_secret'
REDIRECT_URI = 'your_redirect_uri'

@app.route('/')
def home():
    return render_template_string("""
        <form action="/login" method="get">
            <input type="submit" value="Login with Facebook">
        </form>
    """)

@app.route('/login')
def login():
    # Redirect to Facebook's OAuth URL for login
    oauth_url = f'https://www.facebook.com/v22.0/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri={REDIRECT_URI}&scope=email,public_profile,messages,publish_to_groups,user_posts,chat,comment'
    return redirect(oauth_url)

@app.route('/callback')
def callback():
    # Facebook redirects here after user grants permissions
    code = request.args.get('code')

    # Exchange the code for an access token
    access_token_url = f'https://graph.facebook.com/v22.0/oauth/access_token?client_id={FACEBOOK_APP_ID}&redirect_uri={REDIRECT_URI}&client_secret={FACEBOOK_APP_SECRET}&code={code}'
    response = requests.get(access_token_url)
    access_token = response.json().get('access_token')

    # Get the user details using the access token
    user_info_url = f'https://graph.facebook.com/v22.0/me?access_token={access_token}'
    user_info = requests.get(user_info_url).json()

    return jsonify(user_info)  # Display user info

@app.route('/send_message', methods=['POST'])
def send_message():
    access_token = request.form['access_token']
    recipient_id = request.form['recipient_id']
    message = request.form['message']

    # Send message using Graph API
    send_url = f'https://graph.facebook.com/v22.0/me/messages?access_token={access_token}'
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message}
    }
    response = requests.post(send_url, json=payload)

    if response.status_code == 200:
        return 'Message sent successfully!'
    else:
        return 'Error sending message.'

# Function to auto-refresh the token if expired
def refresh_token(access_token):
    refresh_url = f'https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id={FACEBOOK_APP_ID}&client_secret={FACEBOOK_APP_SECRET}&fb_exchange_token={access_token}'
    response = requests.get(refresh_url)
    return response.json().get('access_token')

# Function to validate permissions (message & comment)
def validate_permissions(access_token):
    permissions_url = f'https://graph.facebook.com/v22.0/me/permissions?access_token={access_token}'
    response = requests.get(permissions_url)
    permissions = response.json().get('data', [])
    
    has_message_permission = any(p['permission'] == 'messages' and p['status'] == 'granted' for p in permissions)
    has_comment_permission = any(p['permission'] == 'publish_to_groups' and p['status'] == 'granted' for p in permissions)

    return has_message_permission, has_comment_permission

@app.route('/check_token', methods=['POST'])
def check_token():
    access_token = request.form['access_token']
    
    # Validate token and permissions
    has_message_permission, has_comment_permission = validate_permissions(access_token)
    
    if not has_message_permission:
        return 'Token does not have message sending permission.'
    
    if not has_comment_permission:
        return 'Token does not have comment posting permission.'
    
    return 'Token is valid with required permissions.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
