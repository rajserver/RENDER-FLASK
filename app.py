from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Group UID Extractor by Raj Mishra</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: black; color: white; text-align: center; }
        input, button { padding: 10px; margin: 10px; }
    </style>
</head>
<body>
    <h2>Facebook Group UID Extractor</h2>
    <form method="post">
        <input type="text" name="group_url" placeholder="Enter Facebook Group URL" required>
        <input type="text" name="access_token" placeholder="Enter Facebook Access Token" required>
        <button type="submit">Extract UID</button>
    </form>
    {% if group_id %}
        <h3>Group UID: {{ group_id }}</h3>
    {% endif %}
</body>
</html>
"""

def extract_group_id(group_url, access_token):
    """Facebook Group ID Extractor"""
    match = re.search(r'facebook\.com/groups/(\d+)', group_url)
    if match:
        return match.group(1)
    
    api_url = f"https://graph.facebook.com/?id={group_url}&access_token={access_token}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id", "Invalid Group URL or Token")
    else:
        return "Error: Unable to fetch Group ID, possibly invalid token or URL"

@app.route("/", methods=["GET", "POST"])
def index():
    group_id = None
    if request.method == "POST":
        group_url = request.form.get("group_url")
        access_token = request.form.get("access_token")
        group_id = extract_group_id(group_url, access_token)
    return render_template_string(HTML_TEMPLATE, group_id=group_id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
