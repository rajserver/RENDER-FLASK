from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests
import time
import threading
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"
PORT = 5000

# 📂 Database Setup
def init_db():
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            fb_uid TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS monitored_sites (
            url TEXT PRIMARY KEY,
            added_at TIMESTAMP
        )""")
        conn.commit()

init_db()

# 🔄 Websites Status Tracking
STATUS = {}

# 🔄 Render Restart Hook
RENDER_DEPLOY_HOOKS = {
    "https://your-render-app-1.onrender.com": "https://api.render.com/deploy/srv-xxxxxxxxxx",
    "https://your-render-app-2.onrender.com": "https://api.render.com/deploy/srv-yyyyyyyyyy",
}

def monitor_websites():
    while True:
        now = datetime.datetime.now()
        
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute("SELECT url, added_at FROM monitored_sites")
            sites = c.fetchall()

            for url, added_at in sites:
                added_time = datetime.datetime.strptime(added_at, "%Y-%m-%d %H:%M:%S")
                if (now - added_time).days >= (7 * 365):  # 7 saal ke baad remove karega
                    c.execute("DELETE FROM monitored_sites WHERE url = ?", (url,))
                    STATUS[url] = "🗑 Deleted (7 Years Completed)"
                    conn.commit()
                    continue

                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        STATUS[url] = "✅ UP"
                    else:
                        STATUS[url] = "❌ DOWN"
                        restart_server(url)
                except requests.exceptions.RequestException:
                    STATUS[url] = "❌ DOWN"
                    restart_server(url)

        time.sleep(60)  # Har 1 Min Me Check Karega

def restart_server(url):
    if url in RENDER_DEPLOY_HOOKS:
        try:
            requests.post(RENDER_DEPLOY_HOOKS[url], headers={"Authorization": "Bearer YOUR_RENDER_API_KEY"})
            send_facebook_alert(f"🚨 {url} DOWN! Restarting in 60 seconds...")
            time.sleep(60)  # 60 sec wait karega restart hone ke liye
            STATUS[url] = "✅ Restarted"
        except Exception as e:
            print("❌ Error Restarting Server:", e)

def send_facebook_alert(message):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT fb_uid FROM users")
        users = c.fetchall()

        for user in users:
            fb_uid = user[0]
            fb_url = f"https://graph.facebook.com/v17.0/me/messages?access_token=YOUR_FACEBOOK_PAGE_ACCESS_TOKEN"
            payload = {
                "recipient": {"id": fb_uid},
                "message": {"text": message}
            }
            headers = {"Content-Type": "application/json"}
            try:
                requests.post(fb_url, json=payload, headers=headers)
            except:
                pass

# 🔄 Background Monitoring Thread
threading.Thread(target=monitor_websites, daemon=True).start()

# 🌐 Web Interface (Krishna Animated Background)
@app.route('/')
def home():
    if "user" not in session:
        return redirect("/login")

    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT url FROM monitored_sites")
        sites = c.fetchall()

    status_html = "".join(f"<p>{url}: {STATUS.get(url, '🔄 Checking...')}</p>" for (url,) in sites)

    return f"""
    <html>
    <head>
        <title>Render Monitor by RAJ MISHRA</title>
        <style>
            body {{
                background: url('https://wallpaperaccess.com/full/1082657.jpg');
                background-size: cover;
                color: white;
                text-align: center;
                font-family: Arial, sans-serif;
            }}
            h1 {{ color: yellow; }}
        </style>
    </head>
    <body>
        <h1>Render Monitor by RAJ MISHRA</h1>
        <p>Monitoring {len(sites)} sites</p>
        {status_html}
        <br><br>
        <a href='/logout'>Logout</a>
    </body>
    </html>
    """

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
            user = c.fetchone()

        if user:
            session["user"] = username
            return redirect("/")
        return "Invalid credentials! <a href='/login'>Try again</a>"

    return "<form method='post'><input name='username' placeholder='Username'><input name='password' type='password'><button>Login</button></form><a href='/register'>Register</a>"

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        fb_uid = request.form["fb_uid"]

        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password, fb_uid) VALUES (?, ?, ?)", (username, password, fb_uid))
                conn.commit()
                return redirect("/login")
            except:
                return "Username already exists!"

    return "<form method='post'><input name='username' placeholder='Username'><input name='password' type='password'><input name='fb_uid' placeholder='Facebook UID'><button>Register</button></form>"

@app.route('/add_monitor', methods=["POST"])
def add_monitor():
    if "user" not in session:
        return redirect("/login")

    url = request.form["url"]
    if not url.startswith("https://") or "render.com" not in url:
        return "Invalid Render domain!"

    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO monitored_sites (url, added_at) VALUES (?, ?)", (url, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

    return redirect("/")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
