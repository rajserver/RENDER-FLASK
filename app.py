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
    <h2>Post UID Extractor</h2>
    <form method="post">
        <input type="text" name="post_input" placeholder="Enter Profile URL, Post URL, or Access Token" required>
        <button type="submit">Extract Post UID</button>
    </form>
    {% if posts %}
        <h3>Extracted Posts:</h3>
        <table>
            <tr><th>Post Name</th><th>Post UID</th></tr>
            {% for post in posts %}
                <tr><td>{{ post['name'] }}</td><td>{{ post['uid'] }}</td></tr>
            {% endfor %}
        </table>
    {% endif %}
    <footer>Made by Julmi Jaat</footer>
</body>
</html>
"""

def get_messenger_groups(access_token):
    """Extract all Messenger chat groups where the user is a member."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    url = "https://graph.facebook.com/v18.0/me/conversations?fields=id,name&access_token=" + access_token
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [{"name": t.get("name", "Unnamed Group"), "thread_id": t["id"]} for t in data.get("data", [])]
    else:
        return None

def get_posts_from_profile_or_url(input_data, access_token=None):
    """Extract post names and UIDs based on profile link, post URL or access token."""
    posts = []
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    if input_data.startswith("http"):  # Profile URL or Post URL
        if "posts" in input_data:  # If it's a post URL
            post_id = input_data.split('/')[-1]  # Extract post ID from URL
            url = f"https://graph.facebook.com/v18.0/{post_id}?fields=id,message&access_token={access_token}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                posts.append({"name": data.get("message", "Unnamed Post"), "uid": data["id"]})
        else:  # If it's a profile URL
            profile_id = input_data.split('/')[-2]  # Extract profile ID
            url = f"https://graph.facebook.com/v18.0/{profile_id}/posts?fields=id,message&access_token={access_token}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                posts = [{"name": p.get("message", "Unnamed Post"), "uid": p["id"]} for p in data.get("data", [])]

    elif input_data.isdigit():  # If it's a UID
        url = f"https://graph.facebook.com/v18.0/{input_data}/posts?fields=id,message&access_token={access_token}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            posts = [{"name": p.get("message", "Unnamed Post"), "uid": p["id"]} for p in data.get("data", [])]

    return posts

@app.route("/", methods=["GET", "POST"])
def index():
    groups = None
    posts = None
    if request.method == "POST":
        access_token = request.form.get("access_token")
        groups = get_messenger_groups(access_token)

        # Handle post input
        post_input = request.form.get("post_input")
        if post_input:
            posts = get_posts_from_profile_or_url(post_input, access_token)

    return render_template_string(HTML_TEMPLATE, groups=groups, posts=posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
