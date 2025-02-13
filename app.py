from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import time
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Session ke liye Secret Key

# Store monitored links
monitored_links = {}

# Function to monitor Render links
def monitor_link(link, email):
    while True:
        try:
            response = requests.get(link, timeout=5)
            status_code = response.status_code

            if 200 <= status_code <= 700:
                monitored_links[link]["status"] = f"UP ✅ ({status_code})"
            else:
                monitored_links[link]["status"] = f"DOWN ❌ ({status_code})"
                restart_server(link)
                send_alert(email, "DOWN", link)

            time.sleep(60)  # Check every 60 seconds

        except Exception as e:
            monitored_links[link]["status"] = f"ERROR 🚨 {e}"
            restart_server(link)
            send_alert(email, "DOWN", link)

# Function to keep server active (Ping every 3 minutes)
def keep_server_awake():
    while True:
        requests.get("https://your-deployed-url.onrender.com")  # Replace with actual Render URL
        print("Pinged self to prevent sleep mode! 🔄")
        time.sleep(180)  # Ping every 3 minutes

# Function to restart the server (If needed)
def restart_server(link):
    print(f"Restarting server: {link} 🔄")

# Function to send alerts
def send_alert(email, status, link):
    print(f"Sending alert to {email} - {status} ALERT for {link}")

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
        email = session['email']

        if "render.com" not in link:
            flash("Only Render.com links are allowed!", "danger")
            return redirect(url_for('dashboard'))

        if len(monitored_links) >= 100:
            flash("You can only monitor up to 100 links!", "danger")
            return redirect(url_for('dashboard'))

        monitored_links[link] = {"email": email, "status": "Checking..."}
        threading.Thread(target=monitor_link, args=(link, email)).start()
        flash("Monitoring started!", "success")

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
