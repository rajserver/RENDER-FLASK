from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os
import json
import time
import random
import requests
import threading

app = Flask(__name__)
app.secret_key = os.urandom(24)

monitors = {}

# A mock function to check if server is up or not
def monitor_link(url):
    try:
        response = requests.get(url)
        if response.status_code in range(200, 701):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Function to handle monitoring with auto-recovery
def monitor_and_recover():
    while True:
        for uid, monitor_data in monitors.items():
            url = monitor_data["url"]
            if not monitor_link(url):
                monitors[uid]["status"] = "Down"
                print(f"Monitor {uid} is Down. Trying to recover...")
                # Simulating recovery action
                time.sleep(60)
                monitors[uid]["status"] = "Up"
                print(f"Monitor {uid} is back Up!")
        time.sleep(180)  # Check every 3 minutes

@app.route("/")
def home():
    if 'user_id' in session:
        return render_template("index.html", monitors=monitors)
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "password":  # Placeholder for actual authentication
            session['user_id'] = username
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Here, you would save the username and password (preferably in a database)
        # For simplicity, let's assume you just print them to console
        print(f"New User Registered: {username}, {password}")
        # After registration, you can automatically log in the user or redirect to login
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for("login"))

@app.route("/add_monitor", methods=["POST"])
def add_monitor():
    if 'user_id' in session:
        url = request.form["url"]
        friendly_name = request.form["friendly_name"]
        monitor_id = str(random.randint(1000, 9999))
        monitors[monitor_id] = {
            "url": url,
            "status": "Up",
            "name": friendly_name,
            "created_at": str(datetime.now())
        }
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/edit_monitor/<monitor_id>", methods=["GET", "POST"])
def edit_monitor(monitor_id):
    if 'user_id' in session:
        if request.method == "POST":
            url = request.form["url"]
            friendly_name = request.form["friendly_name"]
            monitors[monitor_id]["url"] = url
            monitors[monitor_id]["name"] = friendly_name
            return redirect(url_for("home"))
        return render_template("edit_monitor.html", monitor=monitors[monitor_id])
    return redirect(url_for("login"))

@app.route("/delete_monitor/<monitor_id>")
def delete_monitor(monitor_id):
    if 'user_id' in session:
        if monitor_id in monitors:
            del monitors[monitor_id]
        return redirect(url_for("home"))
    return redirect(url_for("login"))

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=monitor_and_recover)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    app.run(debug=True, host="0.0.0.0", port=5000)
