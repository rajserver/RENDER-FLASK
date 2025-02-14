from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Messenger Group UID Extractor</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #2c3e50; color: white; text-align: center; }
        input, button { padding: 10px; margin: 10px; }
        table { margin: auto; width: 80%; border-collapse: collapse; background-color: white; color: black; }
        th, td { border: 1px solid black; padding: 10px; text-align: left; }
        footer { text-align: center; font-size: 14px; color: white; margin-top: 20px; }
        header { font-size: 20px; font-weight: bold; color: white; margin-top: 10px; }
    </style>
</head>
<body>
    <header>Made by Julmi Jaat</header>
    <h2>Messenger Chat Group UID Extractor</h2>
    <form method="post">
        <input type="text" name="access_token" placeholder="Enter Facebook Access Token" required>
        <button type="submit">Extract Chat Groups</button>
    </form>
    {% if groups %}
        <h3>Extracted Chat Groups:</h3>
        <table>
            <tr><th>Chat Name</th><th>Thread ID</th></tr>
            {% for group in groups %}
                <tr><td>{{ group['name'] }}</td><td>{{ group['thread_id'] }}</td></tr>
            {% endfor %}
        </table>
    {% endif %}

    <hr>

    <h2>Post UID Extractor from Facebook Profile URL</h2>
    <form method="post">
        <input type="text" name="profile_url" placeholder="Enter Facebook Profile URL" required>
        <button type="submit">Extract Posts from Profile</button>
    </form>
    {% if profile_posts %}
        <h3>Extracted Profile Posts:</h3>
        <table>
            <tr><th>Post Name</th><th>Post UID</th></tr>
            {% for post in profile_posts %}
                <tr><td>{{ post['name'] }}</td><td>{{ post['uid'] }}</td></tr>
            {% endfor %}
        </table>
    {% endif %}

    <hr>

    <h2>Post UID Extractor from Post URL</h2>
    <form method="post">
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required>
        <button type="submit">Extract Post UID</button>
    </form>
    {% if post %}
        <h3>Extracted Post UID:</h3>
        <table>
            <tr><th>Post Name</th><th>Post UID</th></tr>
            <tr><td>{{ post['name'] }}</td><td>{{ post['uid'] }}</td></tr>
        </table>
    {% endif %}

    <hr>

    <h2>Post UID Extractor from Access Token</h2>
    <form method="post">
        <input type="text" name="access_token_for_posts" placeholder="Enter Facebook Access Token" required>
        <button type="submit">Extract Posts from Token</button>
    </form>
    {% if token_posts %}
        <h3>Extracted Posts from Token:</h3>
        <table>
            <tr><th>Post Name</th><th>Post UID</th></tr>
            {% for post in token_posts %}
                <tr><td>{{ post['name'] }}</td><td>{{ post['uid'] }}</td></tr>
            {% endfor %}
        </table>
    {% endif %}

    <footer>Made by Julmi Jaat</footer>
</body>
</html>
"""

def get_messenger_groups(access_token):
    if not access_token:
        return None
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    url = f"https://graph.facebook.com/v17.0/me/conversations?fields=id,name&access_token={access_token}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [{"name": t.get("name", "Unnamed Group"), "thread_id": t["id"]} for t in data.get("data", [])]
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    groups, profile_posts, post, token_posts = None, None, None, None

    if request.method == "POST":
        access_token = request.form.get("access_token")
        groups = get_messenger_groups(access_token)

    return render_template_string(HTML_TEMPLATE, groups=groups)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
