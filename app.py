from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# In-memory dictionary to simulate locked groups (for demo purposes)
locked_groups = {}

# Function to change group name
def change_group_name(token, group_uid, new_group_name):
    url = f'https://graph.facebook.com/v17.0/{group_uid}'
    params = {
        'access_token': token,
        'name': new_group_name
    }
    response = requests.post(url, params=params)
    return response.json()

# Function to lock the group
def lock_group(group_uid):
    locked_groups[group_uid] = True

# Function to check if the group is locked
def is_group_locked(group_uid):
    return locked_groups.get(group_uid, False)

# Function to unlock the group (only by the original admin)
def unlock_group(token, group_uid, admin_uid):
    # Only allow unlock if the admin UID matches
    url = f'https://graph.facebook.com/v17.0/{group_uid}'
    params = {
        'access_token': token,
        'admin_uid': admin_uid  # To check if the admin matches
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # If valid admin UID, unlock the group
        locked_groups[group_uid] = False
        return "Group unlocked successfully!"
    return "Failed to unlock group"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.form['token']
        group_uid = request.form['group_uid']
        new_group_name = request.form['new_group_name']
        admin_uid = request.form['admin_uid']

        # If the group is locked, prevent changes
        if is_group_locked(group_uid):
            return render_template_string(HTML_TEMPLATE, group_response="Group is locked. Cannot change the name.", locked=True)

        # Change group name
        group_response = change_group_name(token, group_uid, new_group_name)
        
        # Lock the group after name change
        lock_group(group_uid)
        
        return render_template_string(HTML_TEMPLATE, group_response=group_response, locked=True)

    return render_template_string(HTML_TEMPLATE, group_response=None, locked=False)

@app.route('/unlock', methods=['POST'])
def unlock():
    token = request.form['token']
    group_uid = request.form['group_uid']
    admin_uid = request.form['admin_uid']

    # Unlock group only if the admin UID is correct
    unlock_response = unlock_group(token, group_uid, admin_uid)
    return render_template_string(HTML_TEMPLATE_UNLOCK, unlock_response=unlock_response)

# HTML Template for Group Lock Page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Group Name Lock by Raj Mishra</title>
</head>
<body>
    <h1>Group Name Lock by Raj Mishra</h1>

    <form method="POST">
        <label for="token">Admin Token:</label><br>
        <input type="text" id="token" name="token" required><br><br>
        
        <label for="group_uid">Group UID:</label><br>
        <input type="text" id="group_uid" name="group_uid" required><br><br>

        <label for="new_group_name">New Group Name:</label><br>
        <input type="text" id="new_group_name" name="new_group_name" required><br><br>

        <label for="admin_uid">Admin UID:</label><br>
        <input type="text" id="admin_uid" name="admin_uid" required><br><br>

        <input type="submit" value="Submit">
    </form>

    {% if group_response %}
        <h3>Group Name Change Response:</h3>
        <pre>{{ group_response }}</pre>
    {% endif %}

    {% if locked %}
        <p>Group name is now locked. No further changes allowed.</p>
    {% endif %}
</body>
</html>
"""

# HTML Template for Unlock Group Page
HTML_TEMPLATE_UNLOCK = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unlock Group by Raj Mishra</title>
</head>
<body>
    <h1>Unlock Group by Raj Mishra</h1>

    <form method="POST" action="/unlock">
        <label for="token">Admin Token:</label><br>
        <input type="text" id="token" name="token" required><br><br>

        <label for="group_uid">Group UID:</label><br>
        <input type="text" id="group_uid" name="group_uid" required><br><br>

        <label for="admin_uid">Admin UID:</label><br>
        <input type="text" id="admin_uid" name="admin_uid" required><br><br>

        <input type="submit" value="Unlock">
    </form>

    {% if unlock_response %}
        <h3>Unlock Response:</h3>
        <pre>{{ unlock_response }}</pre>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
