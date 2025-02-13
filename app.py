from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import time
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key for session management

# Store monitored links
monitored_links = {}

# Function to monitor Render links
def monitor_link(link, email, uid):
    while True:
        try:
            response = requests.get(link, timeout=5)
            status_code = response.status_code

            if status_code >= 200 and status_code <= 700:
                print(f"[{link}] is UP ({status_code}) ✅")
            else:
                print(f"[{link}] is DOWN ({status_code}) ❌ - Restarting...")
                restart_server(link)
                send_alert(uid, email, "DOWN", link)

            time.sleep(60)  # Check every 60 seconds

        except Exception as e:
            print(f"Error monitoring {link}: {e}")
            restart_server(link)
            send_alert(uid, email, "DOWN", link)

# Function to restart the server
def restart_server(link):
    print(f"Restarting server: {link} 🔄")
    # Add Render restart logic here (if required)

# Function to send alerts
def send_alert(uid, email, status, link):
    print(f"Sending alert to {uid} and {email} - {status} ALERT for {link}")

# Homepage
@app.route('/')
def home():
    return render_template('login.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Sign-up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        flash('Account created successfully! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

# Dashboard Page (Monitoring Panel)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        link = request.form['link']
        uid = request.form['uid']
        email = session['email']

        if "render.com" not in link:
            flash("Only Render.com links are allowed!", "danger")
            return redirect(url_for('dashboard'))

        if len(monitored_links) >= 100:
            flash("You can only monitor up to 100 links!", "danger")
            return redirect(url_for('dashboard'))

        monitored_links[link] = {"email": email, "uid": uid}
        threading.Thread(target=monitor_link, args=(link, email, uid)).start()
        flash("Monitoring started!", "success")

    return render_template('dashboard.html', links=monitored_links)

# Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
