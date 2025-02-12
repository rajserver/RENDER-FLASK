from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Messenger Group UID Extractor</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: black; color: white; text-align: center; }
        input, button { padding: 10px; margin: 10px; }
        table { margin: auto; width: 80%; border-collapse: collapse; background-color: white; color: black; }
        th, td { border: 1px solid black; padding: 10px; text-align: left; }
    </style>
</head>
<body>
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
</body>
</html>
"""

def get_messenger_groups(access_token):
    """Extract all Messenger chat groups where the user is a member."""
    url = f"https://graph.facebook.com/me/threads?fields=thread_key,name&access_token={access_token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return [{"name": t["name"], "thread_id": t["thread_key"]} for t in data.get("data", [])]
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    groups = None
    if request.method == "POST":
        access_token = request.form.get("access_token")
        groups = get_messenger_groups(access_token)
    return render_template_string(HTML_TEMPLATE, groups=groups)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
