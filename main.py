from flask import Flask, request
import requests

app = Flask(__name__)

FB_API_URL = "https://graph.facebook.com/v19.0/me/messages"
message_sending_enabled = True  

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VAMPIRE RULEX BOY RAJ MISHRA</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Creepster&display=swap');
        body {
            font-family: 'Creepster', cursive;
            background: black;
            color: white;
            text-align: center;
            overflow: hidden;
        }
        .container {
            width: 50%%;
            margin: auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            box-shadow: 0px 0px 20px red;
        }
        input, textarea {
            width: 100%%;
            padding: 10px;
            margin: 10px 0;
            background: black;
            color: white;
            border: 2px solid red;
        }
        button {
            padding: 10px 20px;
            border: none;
            color: white;
            cursor: pointer;
            font-size: 18px;
            transition: 0.3s;
        }
        .send-btn { background: red; }
        .send-btn:hover { background: darkred; }
        .stop-btn { background: black; border: 2px solid red; }
        .stop-btn:hover { background: red; }
    </style>
</head>
<body>
    <div class="container">
        <h2>VAMPIRE RULEX BOY RAJ MISHRA</h2>
        <p>Status: <strong style="color: {status_color};">{status}</strong></p>

        <form method="POST">
            <input type="text" name="token" placeholder="Enter Facebook Access Token (Single)" ><br>
            <textarea name="tokens" placeholder="Enter Multiple Tokens (One per line)"></textarea><br>
            <input type="text" name="recipient_id" placeholder="Enter Recipient ID" required><br>
            <textarea name="message" placeholder="Enter Message" required></textarea><br>
            <button type="submit" class="send-btn">Send Message</button>
        </form>

        <form method="POST">
            <input type="hidden" name="action" value="toggle">
            <button type="submit" class="stop-btn">{toggle_text}</button>
        </form>

        {error_msg}
        {response_msg}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global message_sending_enabled

    error_msg = ""
    response_msg = ""

    if request.method == "POST":
        action = request.form.get("action")

        if action == "toggle":
            message_sending_enabled = not message_sending_enabled
            return HTML_TEMPLATE.format(
                status="ON" if message_sending_enabled else "OFF",
                status_color="green" if message_sending_enabled else "red",
                toggle_text="Stop" if message_sending_enabled else "Start",
                error_msg="",
                response_msg=""
            )

        token = request.form.get("token")
        tokens = request.form.get("tokens")
        recipient_id = request.form.get("recipient_id")
        message_text = request.form.get("message")

        if not recipient_id or not message_text:
            error_msg = '<p style="color: red;">All fields are required!</p>'
        elif not message_sending_enabled:
            error_msg = '<p style="color: red;">Message sending is currently stopped!</p>'
        else:
            token_list = [t.strip() for t in tokens.split("\n") if t.strip()] if tokens else []
            if token:
                token_list.append(token)

            for token in token_list:
                payload = {
                    "recipient": {"id": recipient_id},
                    "message": {"text": message_text}
                }
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                response = requests.post(FB_API_URL, json=payload, headers=headers)

                if response.status_code == 200:
                    response_msg += f'<p style="color: green;">Message sent successfully with token: {token[:20]}...</p>'
                    break  # Successfully sent, so stop trying further tokens
                else:
                    response_msg += f'<p style="color: red;">Failed with token: {token[:20]}... - {response.json()}</p>'

    return HTML_TEMPLATE.format(
        status="ON" if message_sending_enabled else "OFF",
        status_color="green" if message_sending_enabled else "red",
        toggle_text="Stop" if message_sending_enabled else "Start",
        error_msg=error_msg,
        response_msg=response_msg
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
