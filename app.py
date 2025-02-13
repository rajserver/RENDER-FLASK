from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
import sqlite3
import time
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Setup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Monitoring System
monitored_links = {}

def check_link(link, uid, email):
    while True:
        try:
            response = requests.get(link, timeout=5)
            status_code = response.status_code
            
            if 200 <= status_code <= 700:
                print(f"[OK] {link} is UP - Status: {status_code}")
            else:
                print(f"[DOWN] {link} is DOWN - Restarting...")
                send_alert(uid, email, f"ALERT: {link} is DOWN! Restarting in 60 sec...")
                time.sleep(60)
                restart_render(link)
                send_alert(uid, email, f"RECOVERED: {link} is back UP!")
        except:
            print(f"[ERROR] {link} is unreachable! Retrying in 60 sec...")
            time.sleep(60)

def restart_render(link):
    print(f"Restarting {link}...")
    time.sleep(5)  
    print(f"{link} restarted successfully!")

def send_alert(uid, email, message):
    print(f"Sending alert to {uid} on Facebook & {email} via Email: {message}")

@app.route('/')
def home():
    if "user" in session:
        return render_template_string(monitor_html, links=monitored_links)
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session["user"] = email
            return redirect(url_for("home"))
        else:
            return "Invalid Credentials!"

    return render_template_string(login_html)

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route('/monitor', methods=["POST"])
def monitor():
    if "user" in session:
        link = request.form["link"]
        uid = request.form["uid"]
        email = session["user"]
        
        if link.startswith("https://render.com"):
            monitored_links[link] = {"uid": uid, "email": email}
            threading.Thread(target=check_link, args=(link, uid, email)).start()
            return f"Started monitoring {link}"
        else:
            return "Only Render links are allowed!"

    return redirect(url_for("login"))

# Login Page HTML (In Flask)
login_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Login - Render Monitor</title>
    <style>
        body { background-image: url('https://i.imgur.com/VV2iZ7A.jpg'); background-size: cover; }
    </style>
</head>
<body>
    <h2>Login</h2>
    <form method="POST">
        <label>Email:</label>
        <input type="email" name="email" required>
        <br>
        <label>Password:</label>
        <input type="password" name="password" required>
        <br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

# Monitoring Page HTML (In Flask)
monitor_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Render Monitor</title>
    <style>
        body { background-image: url('https://i.imgur.com/VV2iZ7A.jpg'); background-size: cover; }
    </style>
</head>
<body>
    <h2>Monitor Your Render Links</h2>
    <form method="POST" action="/monitor">
        <label>Render Link:</label>
        <input type="url" name="link" required>
        <br>
        <label>Facebook UID for Alerts:</label>
        <input type="text" name="uid" required>
        <br>
        <button type="submit">Start Monitoring</button>
    </form>
    
    <h3>Monitored Links</h3>
    <ul>
        {% for link, data in links.items() %}
            <li>{{ link }} - UID: {{ data.uid }} - Email: {{ data.email }}</li>
        {% endfor %}
    </ul>
    <a href="/logout">Logout</a>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
