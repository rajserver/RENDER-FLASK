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

    <h2>Post UID Extractor from Facebook Post URL</h2>
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
    {% elif post_error %}
        <p style="color:red;">Error: {{ post_error }}</p>
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

def get_post_from_url(post_url, access_token):
    """Extract post UID and name from a Facebook post URL."""
    post_id = post_url.split('/')[-1]  # Extract post ID from URL
    url = f"https://graph.facebook.com/v18.0/{post_id}?fields=id,message&access_token={access_token}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'message' in data:
            return {"name": data.get("message", "Unnamed Post"), "uid": data["id"]}
        else:
            return {"error": "No message found in the post data."}
    else:
        return {"error": f"Failed to fetch post. Status code: {response.status_code}"}

@app.route("/", methods=["GET", "POST"])
def index():
    groups = None
    post = None
    post_error = None
    
    if request.method == "POST":
        # Get Messenger groups
        access_token = request.form.get("access_token")
        groups = get_messenger_groups(access_token)

        # Get Post from Post URL
        post_url = request.form.get("post_url")
        if post_url:
            post = get_post_from_url(post_url, access_token)
            if "error" in post:
                post_error = post["error"]
            else:
                post = post  # if successful, assign post data

    return render_template_string(HTML_TEMPLATE, groups=groups, post=post, post_error=post_error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
