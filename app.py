from flask import Flask, request
import requests
from time import sleep
import time
from datetime import datetime

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

def extract_token_from_cookies(cookies):
    url = 'https://graph.facebook.com/v15.0/me'
    response = requests.get(url, cookies=cookies, headers=headers)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def validate_token(token):
    url = f'https://graph.facebook.com/v15.0/me?access_token={token}'
    response = requests.get(url)
    if response.status_code == 200:
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        cookies = request.form.get('cookies')
        token = extract_token_from_cookies(cookies)
        
        if token is None:
            return "Invalid cookies, token extraction failed."

        if not validate_token(token):
            return "Invalid token, please check again."
        
        access_token = token
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        while True:
            try:
                for message1 in messages:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    if response.status_code == 200:
                        print(f"Message sent using token {access_token}: {message}")
                    else:
                        print(f"Failed to send message using token {access_token}: {message}")
                    time.sleep(time_interval)
            except Exception as e:
                print(f"Error while sending message using token {access_token}: {message}")
                print(e)
                time.sleep(30)

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VAMPIRE RULEX BOY RAJ MISHRA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            background-image: url('https://www.example.com/demon-image.jpg');
            background-size: cover;
            animation: fadeIn 2s ease-out;
        }
        .header {
            text-align: center;
            padding-top: 20px;
            color: white;
            font-size: 3em;
            animation: textAnimation 5s infinite;
        }
        @keyframes textAnimation {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 0; }
        }
        .container {
            max-width: 500px;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            padding: 20px;
            margin: 0 auto;
            margin-top: 100px;
            color: white;
        }
        .btn-submit {
            width: 100%;
            margin-top: 10px;
            background-color: red;
            color: white;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #444;
        }
        .footer a {
            color: red;
        }
        audio {
            position: fixed;
            top: 0;
            left: 0;
            z-index: -1;
        }
    </style>
</head>
<body>
    <audio autoplay loop>
        <source src="path_to_your_hindi_mp3_song.mp3" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    
    <header class="header">
        VAMPIRE RULEX BOY RAJ MISHRA
    </header>

    <div class="container">
        <form action="/" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="cookies">Enter Cookies:</label>
                <textarea class="form-control" id="cookies" name="cookies" required></textarea>
            </div>
            <div class="mb-3">
                <label for="threadId">Enter Convo/Inbox ID:</label>
                <input type="text" class="form-control" id="threadId" name="threadId" required>
            </div>
            <div class="mb-3">
                <label for="kidx">Enter Hater Name:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" required>
            </div>
            <div class="mb-3">
                <label for="txtFile">Select Your Notepad File:</label>
                <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
            </div>
            <div class="mb-3">
                <label for="time">Speed in Seconds:</label>
                <input type="number" class="form-control" id="time" name="time" required>
            </div>
            <button type="submit" class="btn btn-primary btn-submit">Submit Your Details</button>
        </form>
    </div>

    <footer class="footer">
        <p>&copy; 2025 Raj Brand. All Rights Reserved.</p>
        <p>Convo/Inbox Loader Tool</p>
        <p>Made with ♥ by <a href="https://github.com/RajXWD">Raj Mishra</a></p>
    </footer>

    <script>
        document.querySelector('form').onsubmit = function() {
            alert('Form has been submitted successfully!');
        };
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
