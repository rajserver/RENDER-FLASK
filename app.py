from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TOKEN EXTRACTOR BY RAJ MISHRA</title>
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
                    overflow: hidden;
                    animation: backgroundMove 10s linear infinite;
                }

                @keyframes backgroundMove {
                    0% {
                        background-color: black;
                    }
                    50% {
                        background-color: darkred;
                    }
                    100% {
                        background-color: black;
                    }
                }

                .text {
                    font-size: 2rem;
                    font-weight: bold;
                    letter-spacing: 2px;
                    text-align: center;
                    animation: textAnimation 10s infinite;
                }

                @keyframes textAnimation {
                    0% {
                        color: white;
                    }
                    25% {
                        color: red;
                    }
                    50% {
                        color: yellow;
                    }
                    75% {
                        color: blue;
                    }
                    100% {
                        color: white;
                    }
                }

                .letter {
                    display: inline-block;
                    opacity: 0;
                    animation: letterFadeIn 1.5s forwards;
                }

                @keyframes letterFadeIn {
                    0% {
                        opacity: 0;
                    }
                    100% {
                        opacity: 1;
                    }
                }

                form {
                    margin-top: 20px;
                    text-align: center;
                }

                textarea {
                    width: 300px;
                    height: 100px;
                }

                input[type="submit"] {
                    margin-top: 10px;
                    padding: 10px 20px;
                    background-color: darkred;
                    border: none;
                    color: white;
                    cursor: pointer;
                }

                input[type="submit"]:hover {
                    background-color: red;
                }

                a {
                    color: white;
                    text-decoration: none;
                    margin-top: 20px;
                    display: block;
                    text-align: center;
                }

                a:hover {
                    color: lightblue;
                }

                .token-checker {
                    margin-top: 40px;
                    text-align: center;
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
                }

                .token-checker input[type="submit"]:hover {
                    background-color: darkgreen;
                }
            </style>
        </head>
        <body>
            <div class="text">
                <span class="letter" style="animation-delay: 0s;">V</span>
                <span class="letter" style="animation-delay: 0.2s;">A</span>
                <span class="letter" style="animation-delay: 0.4s;">M</span>
                <span class="letter" style="animation-delay: 0.6s;">P</span>
                <span class="letter" style="animation-delay: 0.8s;">I</span>
                <span class="letter" style="animation-delay: 1s;">R</span>
                <span class="letter" style="animation-delay: 1.2s;">E</span>
                <span class="letter" style="animation-delay: 1.4s;"> </span>
                <span class="letter" style="animation-delay: 1.6s;">R</span>
                <span class="letter" style="animation-delay: 1.8s;">U</span>
                <span class="letter" style="animation-delay: 2s;">L</span>
                <span class="letter" style="animation-delay: 2.2s;">E</span>
                <span class="letter" style="animation-delay: 2.4s;">X</span>
                <span class="letter" style="animation-delay: 2.6s;"> </span>
                <span class="letter" style="animation-delay: 2.8s;">B</span>
                <span class="letter" style="animation-delay: 3s;">O</span>
                <span class="letter" style="animation-delay: 3.2s;">Y</span>
                <span class="letter" style="animation-delay: 3.4s;"> </span>
                <span class="letter" style="animation-delay: 3.6s;">R</span>
                <span class="letter" style="animation-delay: 3.8s;">A</span>
                <span class="letter" style="animation-delay: 4s;">J</span>
                <span class="letter" style="animation-delay: 4.2s;"> </span>
                <span class="letter" style="animation-delay: 4.4s;">M</span>
                <span class="letter" style="animation-delay: 4.6s;">I</span>
                <span class="letter" style="animation-delay: 4.8s;">S</span>
                <span class="letter" style="animation-delay: 5s;">H</span>
                <span class="letter" style="animation-delay: 5.2s;">R</span>
                <span class="letter" style="animation-delay: 5.4s;">A</span>
            </div>

            <!-- Cookies to Token Form -->
            <h2>Cookies to Token</h2>
            <form action="/get_token" method="POST">
                <label for="cookies">Enter Cookies:</label>
                <textarea name="cookies" rows="5" cols="50"></textarea><br><br>
                <input type="submit" value="Get Token">
            </form>

            <!-- Instagram Permission Section -->
            <h2>Instagram Permission</h2>
            <p>Click below to grant Instagram permissions for your token:</p>
            <a href="/instagram_permission">Grant Instagram Permission</a>

            <!-- Token Checker Section -->
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

@app.route('/get_token', methods=['POST'])
def get_token():
    cookies = request.form['cookies']
    token = extract_token_from_cookies(cookies)
    return render_template_string('''
        <h1>Token Extracted</h1>
        <p>Token: {{ token }}</p>
        <a href="/">Back</a>
    ''', token=token)

def extract_token_from_cookies(cookies):
    # Logic to extract token from cookies
    # Example extraction; replace with actual logic
    return "extracted_token_from_cookies"

@app.route('/instagram_permission')
def instagram_permission():
    # Logic to handle Instagram permission granting (OAuth)
    # Provide Instagram OAuth URL here for permission
    instagram_oauth_url = "https://www.instagram.com/oauth/authorize"  # Example URL
    return redirect(instagram_oauth_url)

@app.route('/check_token', methods=['POST'])
def check_token():
    token = request.form['token']
    token_details = check_token_details(token)
    return render_template_string('''
        <h1>Token Checker</h1>
        {% if token_details['valid'] %}
            <p>Name: {{ token_details['name'] }}</p>
            <p>Email: {{ token_details['email'] }}</p>
            <p>UID: {{ token_details['uid'] }}</p>
            <p>Message Permission: {{ token_details['can_send_message'] }}</p>
            <p>Comment Permission: {{ token_details['can_comment'] }}</p>
            <img src="{{ token_details['profile_pic'] }}" alt="Profile Picture">
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
        can_send_message = "Yes" if "message_send_permission" in data else "No"
        can_comment = "Yes" if "comment_permission" in data else "No"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
