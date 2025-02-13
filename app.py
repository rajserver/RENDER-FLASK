from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
import sqlite3
import time
import threading
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Setup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS monitors (id INTEGER PRIMARY KEY, link TEXT, uid TEXT, email TEXT, expiry_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Monitoring System
monitored_links = {}

def check_link(link, uid, email):
    expiry_date = datetime.now() + timedelta(days=2555)  # 7 years monitoring
    while datetime.now() < expiry_date:
        try:
            response = requests.get(link, timeout=5)
            status_code = response.status_code
            
            if 200 <= status_code <= 700:
                print(f"[OK] {link} is UP - Status: {status_code}")
            else:
                print(f"[DOWN] {link} is DOWN - Restarting...")
                send_alert(uid, email, f"⚠️ ALERT: {link} is DOWN! Restarting in 60 sec...")
                time.sleep(60)
                restart_render(link)
                send_alert(uid, email, f"✅ RECOVERED: {link} is back UP!")
        except:
            print(f"[ERROR] {link} is unreachable! Retrying in 60 sec...")
            time.sleep(60)

def restart_render(link):
    print(f"Restarting {link}...")
    time.sleep(5)  
    print(f"{link} restarted successfully!")

def send_alert(uid, email, message):
    print(f"🔔 Sending alert to {uid} on Facebook & {email} via Email: {message}")

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

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template_string(signup_html)

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
        
        if link.startswith("https://render.com/"):  # Only Render Links Allowed
            expiry_date = (datetime.now() + timedelta(days=2555)).strftime("%Y-%m-%d")  
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO monitors (link, uid, email, expiry_date) VALUES (?, ?, ?, ?)", (link, uid, email, expiry_date))
            conn.commit()
            conn.close()

            monitored_links[link] = threading.Thread(target=check_link, args=(link, uid, email))
            monitored_links[link].start()

            return f"✅ {link} added for monitoring!"
        else:
            return "❌ Only Render.com links are allowed!"

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
