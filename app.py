from flask import Flask, request, redirect, url_for, render_template_string
import requests
import time
import random
import string
import multiprocessing

app = Flask(__name__)

# Task Dictionary to store running processes
running_tasks = {}

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

def generate_task_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def post_comments(task_id, method, thread_id, haters_name, time_interval, credentials, credentials_type, comments):
    num_comments = len(comments)
    num_credentials = len(credentials)
    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    
    while task_id in running_tasks:
        try:
            for comment_index in range(num_comments):
                if task_id not in running_tasks:
                    print(f"[+] Task {task_id} Stopped Successfully!")
                    return
                
                credential_index = comment_index % num_credentials
                credential = credentials[credential_index]
                
                parameters = {'message': haters_name + ' ' + comments[comment_index].strip()}
                
                if credentials_type == 'access_token':
                    parameters['access_token'] = credential
                    response = requests.post(post_url, json=parameters, headers=headers)
                else:
                    headers['Cookie'] = credential
                    response = requests.post(post_url, data=parameters, headers=headers)

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Comment No. {} Post Id {} Credential No. {}: {}".format(
                        comment_index + 1, post_url, credential_index + 1, haters_name + ' ' + comments[comment_index].strip()))
                    print("  - Time: {}".format(current_time))
                    print("\n" * 2)
                else:
                    print("[x] Failed to send Comment No. {} Post Id {} Credential No. {}: {}".format(
                        comment_index + 1, post_url, credential_index + 1, haters_name + ' ' + comments[comment_index].strip()))
                    print("  - Time: {}".format(current_time))
                    print("\n" * 2)
                time.sleep(time_interval)
        except Exception as e:
            print(e)
            time.sleep(30)

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝐉𝐔𝐋𝐌𝐈 𝐉𝐀𝐀𝐓</title>
</head>
<body>
    <h1>𝐓𝐇𝐄 𝐋𝐄𝐆𝐄𝐍𝐃 𝐉𝐔𝐋𝐌𝐈 𝐉𝐀𝐀𝐓</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <label>ᴘᴏꜱᴛ ɪᴅ</label>
        <input type="text" name="threadId" required><br>
        <label>ʜᴀᴛᴇʀ ɴᴀᴍᴇ</label>
        <input type="text" name="kidx" required><br>
        <label>𝐂𝐇𝐎𝐎𝐒𝐄 𝐌𝐄𝐓𝐇𝐎𝐃</label>
        <select name="method" required>
            <option value="token">ᴛᴏᴋᴇɴ</option>
            <option value="cookies">ᴄᴏᴏᴋɪᴇꜱ</option>
        </select><br>
        <label>ꜱᴇʟᴇᴄᴛ ᴛᴏᴋᴇɴ ꜰɪʟᴇ</label>
        <input type="file" name="tokenFile" accept=".txt"><br>
        <label>ꜱᴇʟᴇᴄᴛ ᴄᴏᴏᴋɪᴇꜱ ꜰɪʟᴇ</label>
        <input type="file" name="cookiesFile" accept=".txt"><br>
        <label>ꜱᴇʟᴇᴄᴛ ᴄᴏᴍᴍᴇɴᴛꜱ ꜰɪʟᴇ</label>
        <input type="file" name="commentsFile" accept=".txt" required><br>
        <label>ᴛɪᴍᴇ(20s ᴍɪɴ)</label>
        <input type="number" name="time" required><br>
        <button type="submit">𝐒𝐓𝐀𝐑𝐓 𝐏𝐎𝐒𝐓𝐈𝐍𝐆</button>
    </form>

    <h2>𝐒𝐓𝐎𝐏 𝐀𝐍𝐘 𝐑𝐔𝐍𝐍𝐈𝐍𝐆 𝐓𝐀𝐒𝐊</h2>
    <form action="/stop" method="post">
        <label>𝐄𝐍𝐓𝐄𝐑 𝐓𝐀𝐒𝐊 𝐈𝐃 𝐓𝐎 𝐒𝐓𝐎𝐏</label>
        <input type="text" name="task_id" required>
        <button type="submit">𝐒𝐓𝐎𝐏 𝐓𝐀𝐒𝐊</button>
    </form>
</body>
</html>
''')

@app.route('/', methods=['POST'])
def start_task():
    method = request.form.get('method')
    thread_id = request.form.get('threadId')
    haters_name = request.form.get('kidx')
    time_interval = int(request.form.get('time'))

    comments_file = request.files['commentsFile']
    comments = comments_file.read().decode().splitlines()

    if method == 'token':
        token_file = request.files['tokenFile']
        credentials = token_file.read().decode().splitlines()
        credentials_type = 'access_token'
    else:
        cookies_file = request.files['cookiesFile']
        credentials = cookies_file.read().decode().splitlines()
        credentials_type = 'Cookie'

    task_id = generate_task_id()
    process = multiprocessing.Process(target=post_comments, args=(task_id, method, thread_id, haters_name, time_interval, credentials, credentials_type, comments))
    process.start()

    running_tasks[task_id] = process
    return f"Task Started! Task ID: {task_id}"

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('task_id')
    
    if task_id in running_tasks:
        running_tasks[task_id].terminate()
        del running_tasks[task_id]
        return f"Task {task_id} Stopped Successfully!"
    return "Invalid Task ID!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
