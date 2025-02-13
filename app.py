from flask import Flask, render_template, request, redirect, session
import requests, sqlite3, datetime, time
import threading

app = Flask(__name__)
app.secret_key = "rajmishra_secret_key"
STATUS = {}

# Database Setup
def init_db():
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS monitored_sites (id INTEGER PRIMARY KEY, user_email TEXT, url TEXT, fb_uid TEXT, added_at TEXT)''')
        conn.commit()

init_db()

# Monitor Function
def monitor_websites():
    while True:
        now = datetime.datetime.now()

        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute("SELECT url, fb_uid, user_email, added_at FROM monitored_sites")
            sites = c.fetchall()

            for url, fb_uid, user_email, added_at in sites:
                added_time = datetime.datetime.strptime(added_at, "%Y-%m-%d %H:%M:%S")
                if (now - added_time).days >= (7 * 365):
                    c.execute("DELETE FROM monitored_sites WHERE url=?", (url,))
                    STATUS[url] = "🗑 Deleted (7 Years Completed)"
                    conn.commit()
                    continue

                try:
                    response = requests.get(url, timeout=10)
                    status_code = response.status_code

                    if 200 <= status_code <= 700:  # Accepts any code between 200-700
                        if STATUS.get(url) == "❌ DOWN":
                            send_alerts(f"✅ {url} RECOVERED! Incident Resolved.", fb_uid, user_email)
                        STATUS[url] = f"✅ UP (Status {status_code})"
                    else:
                        if STATUS.get(url) == "✅ UP":
                            send_alerts(f"🚨 {url} DOWN! Restarting in 60 seconds...", fb_uid, user_email)
                        STATUS[url] = f"❌ DOWN (Status {status_code})"
                        restart_server(url)

                except requests.exceptions.RequestException:
                    if STATUS.get(url) == "✅ UP":
                        send_alerts(f"🚨 {url} DOWN! Restarting in 60 seconds...", fb_uid, user_email)
                    STATUS[url] = "❌ DOWN"
                    restart_server(url)

        time.sleep(60)

# Send Alerts (Facebook & Email)
def send_alerts(message, fb_uid, user_email):
    if fb_uid:
        send_facebook_message(fb_uid, message)
    if user_email:
        send_email_alert(user_email, message)

# Restart Server Function (Auto-Recovery)
def restart_server(url):
    time.sleep(60)  # 60 Sec Delay Before Restart
    requests.get(url)  # Restarting the Render Server

# Facebook Messenger Alert Function
def send_facebook_message(uid, message):
    fb_token = "YOUR_FACEBOOK_ACCESS_TOKEN"
    fb_url = f"https://graph.facebook.com/v17.0/{uid}/messages"
    payload = {"message": message, "access_token": fb_token}
    requests.post(fb_url, data=payload)

# Email Alert Function
def send_email_alert(email, message):
    print(f"📩 Alert Sent to {email}: {message}")

# Background Monitoring Thread
threading.Thread(target=monitor_websites, daemon=True).start()

# Flask Routes
@app.route("/")
def home():
    if "email" in session:
        user_email = session["email"]
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute("SELECT url, fb_uid FROM monitored_sites WHERE user_email=?", (user_email,))
            sites = c.fetchall()
        return render_template("index.html", sites=sites, user_email=user_email)
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = c.fetchone()
        if user:
            session["email"] = email
            return redirect("/")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/login")

@app.route("/add_monitor", methods=["POST"])
def add_monitor():
    if "email" in session:
        user_email = session["email"]
        url = request.form["url"]
        fb_uid = request.form["fb_uid"]
        added_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "render.com" not in url:
            return "❌ Only Render URLs are allowed!"
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO monitored_sites (user_email, url, fb_uid, added_at) VALUES (?, ?, ?, ?)", (user_email, url, fb_uid, added_at))
            conn.commit()
        return redirect("/")
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
