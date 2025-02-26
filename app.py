from flask import Flask, request, redirect, url_for, render_template_string
import requests
import time
import threading
import uuid

app = Flask(__name__)

headers_template = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

running_tasks = {}

def extract_token(file):
    content = file.read().decode('utf-8').strip()
    if 'c_user=' in content and 'xs=' in content:
        return "ExtractedTokenFromCookies"  # Yahan cookies se token extract karna hoga
    return content  # Agar direct token diya gaya hai to use return karenge

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝐉𝐔𝐋𝐌𝐈 𝐉𝐀𝐀𝐓</title>
    <style>
        body {
            background-image: url('https://i.ibb.co/sRZFHxL/2acadd2ebf64721bab65d62b844e54c5.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 40px auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .form-control {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: none;
        }
        .btn-submit {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            width: 100%;
        }
        footer {
            text-align: center;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.7);
            margin-top: auto;
        }
        footer p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <header class="header">
        <h1 style="color: red;"> 𝐓𝐇𝐄 𝐋𝐄𝐆𝐄𝐍𝐃 𝐉𝐔𝐋𝐌𝐈 𝐉𝐀𝐀𝐓</h1>
        <h1 style="color: blue;">𝐉𝐔𝐋𝐌𝐈 𝐏𝐎𝐒𝐓 𝐒𝐄𝐑𝐕𝐄𝐑 (𝐎𝐅𝐅𝐋𝐈𝐍𝐄-𝐂𝐎𝐍𝐕𝐎)</h1>
    </header>

    <div class="container">
        <form action="/" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="threadId">ᴩᴏꜱᴛ ɪᴅ</label>
                <input type="text" class="form-control" id="threadId" name="threadId" required>
            </div>
            <div class="mb-3">
                <label for="tokenFile">ᴜᴩʟᴏᴀᴅ ᴛᴏᴋᴇɴ/ᴄᴏᴏᴋɪᴇꜱ ꜰɪʟᴇ</label>
                <input type="file" class="form-control" id="tokenFile" name="tokenFile" required>
            </div>
            <div class="mb-3">
                <label for="kidx">ᴇɴᴛᴇʀ ʏᴏᴜʀ/ʜᴀᴛᴇʀ ɴᴀᴍᴇ</label>
                <input type="text" class="form-control" id="kidx" name="kidx" required>
            </div>
            <div class="mb-3">
                <label for="time">ᴛɪᴍᴇ(20ꜱᴇᴄᴏɴᴅꜱ ᴍɪɴɪᴍᴜᴍ)</label>
                <input type="number" class="form-control" id="time" name="time" required>
            </div>
            <button type="submit" class="btn-submit">𝐒𝐓𝐀𝐑𝐓</button>
        </form>

        <h3>Task ID: <span id="taskId"></span></h3>
        
        <form action="/stop" method="post">
            <label for="stopTaskId">Enter Task ID to Stop:</label>
            <input type="text" class="form-control" id="stopTaskId" name="taskId" required>
            <button type="submit" class="btn-submit" style="background-color: red;">𝐒𝐓𝐎𝐏</button>
        </form>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const params = new URLSearchParams(window.location.search);
            if (params.has('taskId')) {
                document.getElementById('taskId').textContent = params.get('taskId');
            }
        });
    </script>
</body>
</html>
''')

def comment_task(task_id, thread_id, token, mn, time_interval):
    headers = headers_template.copy()
    headers['Authorization'] = f'Bearer {token}'
    
    comments = ["Sample Comment 1", "Sample Comment 2"]  
    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    
    while task_id in running_tasks:
        for comment in comments:
            if task_id not in running_tasks:
                break
            parameters = {'message': mn + ' ' + comment}
            response = requests.post(post_url, json=parameters, headers=headers)
            print(f"[+] Comment Sent: {parameters['message']}")
            time.sleep(time_interval)

@app.route('/', methods=['POST'])
def start_task():
    thread_id = request.form.get('threadId')
    mn = request.form.get('kidx')
    time_interval = int(request.form.get('time'))
    
    if 'tokenFile' not in request.files:
        return "No file uploaded!"
    
    file = request.files['tokenFile']
    token = extract_token(file)
    
    task_id = str(uuid.uuid4())[:8]
    running_tasks[task_id] = True
    threading.Thread(target=comment_task, args=(task_id, thread_id, token, mn, time_interval), daemon=True).start()
    
    return redirect(url_for('index', taskId=task_id))

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in running_tasks:
        del running_tasks[task_id]
        return f"Task {task_id} Stopped!"
    return "Invalid Task ID!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
