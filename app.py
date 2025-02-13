from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import time
import threading
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Store monitored links
monitored_links = {}

# Function to monitor Render links
def monitor_link(link, name):
    start_time = datetime.now()
    while True:
        try:
            response = requests.get(link, timeout=5)
            status_code = response.status_code

            if 200 <= status_code <= 700:
                uptime_duration = datetime.now() - start_time
                monitored_links[link]["status"] = f"UP ✅ ({status_code})"
                monitored_links[link]["uptime"] = str(uptime_duration).split(".")[0]
            else:
                monitored_links[link]["status"] = f"DOWN ❌ ({status_code})"

            time.sleep(60)  # Check every 60 seconds

        except Exception:
            monitored_links[link]["status"] = "ERROR 🚨 (Unable to Reach)"
            time.sleep(60)

# Function to keep server active (Ping every 3 minutes)
def keep_server_awake():
    while True:
        requests.get("https://your-deployed-url.onrender.com")  # Replace with actual Render URL
        print("Pinged self to prevent sleep mode! 🔄")
        time.sleep(180)  # Ping every 3 minutes

# Homepage
@app.route('/')
def home():
    if 'email' in session:
        return redirect(url_for('dashboard'))  # Auto redirect to Dashboard if already logged in
    return redirect(url_for('login'))

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:  
        return redirect(url_for('dashboard'))  # Already logged in, go to dashboard

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session['email'] = email  # Store login session
        flash("Login successful!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

# Sign-up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        flash('Account created successfully! Please login.', "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

# Dashboard Page (Monitoring Panel)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        link = request.form['link']
        name = request.form['name']

        if "render.com" not in link:
            flash("Only Render.com links are allowed!", "danger")
            return redirect(url_for('dashboard'))

        if len(monitored_links) >= 100:
            flash("You can only monitor up to 100 links!", "danger")
            return redirect(url_for('dashboard'))

        monitored_links[link] = {"name": name, "status": "Checking...", "uptime": "0 sec"}
        threading.Thread(target=monitor_link, args=(link, name)).start()
        flash(f"Monitoring started for '{name}'!", "success")

    return render_template('dashboard.html', links=monitored_links)

# Logout (Clears Session)
@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("You have been logged out!", "info")
    return redirect(url_for('login'))

# Start pinging to keep server awake
threading.Thread(target=keep_server_awake, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
