from flask import Flask, request
import threading
import time
import subprocess
import requests
import re

app = Flask(__name__)

# Store monitored URLs and scripts
monitors = []

# Function to check URL status & auto-restart script if down
def monitor_replit(url, script, index):
    start_time = time.time()
    while True:
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
        except:
            status_code = 0  # Down hai
        
        if 200 <= status_code <= 600:
            server_status = "🟢 UP"
        else:
            server_status = "🔴 DOWN"
            subprocess.run(["python3", script], check=False)  # Auto Restart

        uptime_days = int((time.time() - start_time) / 86400)  # Days uptime

        monitors[index]["status"] = server_status
        monitors[index]["uptime"] = uptime_days
        monitors[index]["status_code"] = status_code

        time.sleep(60)  # Har 1 min me check karega

# Route to add new URL & script
@app.route('/add', methods=['POST'])
def add_monitor():
    url = request.form['url']
    script = request.form['script']
    
    # ✅ **Check if URL follows Replit format**
    if not re.match(r"https://.*\.replit\.dev", url):
        return "<script>alert('❌ Error: Only replit.dev URLs are allowed!'); window.location.href='/'</script>"
    
    monitor = {
        "index": len(monitors) + 1,
        "url": url,
        "script": script,
        "status": "Checking...",
        "uptime": 0,
        "status_code": "N/A"
    }
    monitors.append(monitor)
    
    # Start monitoring in background
    thread = threading.Thread(target=monitor_replit, args=(url, script, len(monitors) - 1))
    thread.daemon = True
    thread.start()
    
    return "<script>window.location.href='/'</script>"

# Web UI
@app.route('/')
def index():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Replit Auto Monitor</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: black;
                color: white;
            }}
            table {{
                width: 90%;
                margin: auto;
                border-collapse: collapse;
                margin-top: 20px;
                background-color: #222;
            }}
            th, td {{
                border: 1px solid white;
                padding: 10px;
            }}
            .up {{ color: green; }}
            .down {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>Replit Auto Monitor</h1>
        <form action="/add" method="post">
            <label>Replit URL:</label>
            <input type="text" name="url" required placeholder="https://your-replit.replit.dev">
            <label>Replit Script Path:</label>
            <input type="text" name="script" required placeholder="your_script.py">
            <button type="submit">Add Monitor</button>
        </form>

        <h2>Monitored URLs</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Replit URL</th>
                <th>Status</th>
                <th>Uptime (Days)</th>
                <th>Status Code</th>
                <th>Script</th>
            </tr>
            {"".join([
                f"<tr><td>{m['index']}</td><td>{m['url']}</td><td class='{'up' if m['status'] == '🟢 UP' else 'down'}'>{m['status']}</td><td>{m['uptime']}</td><td>{m['status_code']}</td><td>{m['script']}</td></tr>"
                for m in monitors
            ])}
        </table>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
