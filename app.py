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
    """Extract all Messenger chat groups where the user is a member."""
    if not access_token:
        return None  # If access token is not provided, return None
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    url = f"https://graph.facebook.com/v18.0/me/conversations?fields=id,name&access_token={access_token}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [{"name": t.get("name", "Unnamed Group"), "thread_id": t["id"]} for t in data.get("data", [])]
    else:
        return None

def get_posts_from_profile(profile_url, access_token):
    """Extract all posts from a Facebook profile URL."""
    profile_id = profile_url.split('/')[-2]  # Extract profile ID
    url = f"https://graph.facebook.com/v18.0/{profile_id}/posts?fields=id,message&access_token={access_token}"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})

    if response.status_code == 200:
        data = response.json()
        return [{"name": p.get("message", "Unnamed Post"), "uid": p["id"]} for p in data.get("data", [])]
    else:
        return None

def get_post_from_url(post_url, access_token):
    """Extract post UID and name from a Facebook post URL."""
    post_id = post_url.split('/')[-1]  # Extract post ID
    url = f"https://graph.facebook.com/v18.0/{post_id}?fields=id,message&access_token={access_token}"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})

    if response.status_code == 200:
        data = response.json()
        return {"name": data.get("message", "Unnamed Post"), "uid": data["id"]}
    else:
        return None

def get_posts_from_token(access_token_for_posts):
    """Extract all posts using Facebook access token."""
    url = f"https://graph.facebook.com/v18.0/me/posts?fields=id,message&access_token={access_token_for_posts}"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token_for_posts}"})

    if response.status_code == 200:
        data = response.json()
        return [{"name": p.get("message", "Unnamed Post"), "uid": p["id"]} for p in data.get("data", [])]
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    groups = None
    profile_posts = None
    post = None
    token_posts = None
    
    if request.method == "POST":
        access_token = request.form.get("access_token")
        groups = get_messenger_groups(access_token)

        profile_url = request.form.get("profile_url")
        if profile_url:
            profile_posts = get_posts_from_profile(profile_url, access_token)

        post_url = request.form.get("post_url")
        if post_url:
            post = get_post_from_url(post_url, access_token)

        access_token_for_posts = request.form.get("access_token_for_posts")
        if access_token_for_posts:
            token_posts = get_posts_from_token(access_token_for_posts)

    return render_template_string(HTML_TEMPLATE, groups=groups, profile_posts=profile_posts, post=post, token_posts=token_posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
