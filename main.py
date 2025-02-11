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
            position: relative;
            z-index: 10;
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

        /* Horror Animation */
        @keyframes flicker {
            0% { opacity: 0.1; }
            50% { opacity: 1; }
            100% { opacity: 0.1; }
        }

        .flicker-text {
            font-size: 30px;
            color: red;
            text-shadow: 0px 0px 10px red;
            animation: flicker 1s infinite alternate;
        }

        /* Moving Background */
        .horror-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%%;
            height: 100%%;
            background: url('https://i.gifer.com/7R84.gif') no-repeat center center fixed;
            background-size: cover;
            opacity: 0.3;
            z-index: -1;
        }

        /* Ghost Effect */
        .ghost {
            position: fixed;
            width: 100px;
            height: 100px;
            background: url('https://i.gifer.com/origin/8f/8f2170558b258f4b4c1367cdbf4903b9_w200.gif') no-repeat;
            background-size: cover;
            top: 20%%;
            left: 40%%;
            animation: floatGhost 3s infinite alternate ease-in-out;
        }

        @keyframes floatGhost {
            0% { transform: translateY(0px); }
            100% { transform: translateY(20px); }
        }

    </style>
</head>
<body>
    <div class="horror-bg"></div>
    <div class="ghost"></div>
    <audio autoplay loop>
        <source src="https://www.fesliyanstudios.com/play-mp3/387" type="audio/mpeg">
    </audio>

    <div class="container">
        <h2 class="flicker-text">VAMPIRE RULEX BOY RAJ MISHRA</h2>
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
                status="ON" if message_sending_enabled
