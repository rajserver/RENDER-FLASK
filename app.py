import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Facebook Graph API URL
GRAPH_API_URL = 'https://graph.facebook.com/'

# Store the locked state and admin UID in a dictionary (can be replaced with a database in a real-world scenario)
locked_groups = {}

def update_group_name(group_uid, access_token, new_group_name):
    # API call to update the group name
    url = f'{GRAPH_API_URL}{group_uid}'
    params = {
        'access_token': access_token,
        'name': new_group_name
    }
    response = requests.post(url, params=params)
    return response.json()

def update_nickname(user_uid, access_token, new_nickname):
    # API call to update the nickname
    url = f'{GRAPH_API_URL}{user_uid}'
    params = {
        'access_token': access_token,
        'nickname': new_nickname
    }
    response = requests.post(url, params=params)
    return response.json()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        group_uid = request.form["group_uid"]
        admin_uid = request.form["admin_uid"]
        new_group_name = request.form["new_group_name"]
        new_nickname = request.form["new_nickname"]
        access_token = request.form["access_token"]
        action = request.form["action"]  # lock or unlock

        # Check if the token belongs to any group member (for changing the group name and nickname)
        group_check_url = f'{GRAPH_API_URL}{group_uid}'
        group_check_params = {
            'access_token': access_token
        }
        group_check_response = requests.get(group_check_url, params=group_check_params)
        group_check_data = group_check_response.json()

        if 'error' in group_check_data:
            return render_template_string("""
                <html>
                    <body>
                        <h1>Permission Error</h1>
                        <p>Your token is invalid or does not belong to the group. Please provide a valid token.</p>
                    </body>
                </html>
            """)

        # Check if the token belongs to the admin (for locking/unlocking)
        admin_check_url = f'{GRAPH_API_URL}{admin_uid}'
        admin_check_params = {
            'access_token': access_token
        }
        admin_check_response = requests.get(admin_check_url, params=admin_check_params)
        admin_check_data = admin_check_response.json()

        if 'error' in admin_check_data:
            return render_template_string("""
                <html>
                    <body>
                        <h1>Permission Error</h1>
                        <p>Your token does not belong to the admin. Please provide a valid admin token.</p>
                    </body>
                </html>
            """)

        if action == "lock":
            # Lock the group name and nickname (only by admin)
            if group_uid not in locked_groups:
                locked_groups[group_uid] = {
                    'admin_uid': admin_uid,
                    'group_name': new_group_name,
                    'nickname': new_nickname
                }
                group_response = update_group_name(group_uid, access_token, new_group_name)
                nickname_response = update_nickname(admin_uid, access_token, new_nickname)

                if 'error' not in group_response and 'error' not in nickname_response:
                    response_message = f"Group name and nickname have been successfully locked to '{new_group_name}' and '{new_nickname}', and they are now locked by admin UID {admin_uid}."
                else:
                    response_message = "Error updating the group name or nickname. Please check the details."
            else:
                response_message = "Group is already locked. Only the admin can unlock it."

        elif action == "unlock":
            # Unlock the group name and nickname (only by admin)
            if group_uid in locked_groups and locked_groups[group_uid]['admin_uid'] == admin_uid:
                del locked_groups[group_uid]  # Remove lock
                response_message = f"Group name and nickname have been successfully unlocked by admin UID {admin_uid}."
            else:
                response_message = "This group is not locked, or you are not the admin."

        # Return the response with the lock/unlock and name change confirmation
        return render_template_string("""
            <html>
                <head>
                    <title>Group Name Lock and Change by Raj</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f2f2f2;
                            color: #333;
                            padding: 20px;
                            text-align: center;
                        }
                        h1 {
                            color: #ff6600;
                        }
                        input[type="text"], input[type="submit"], select {
                            padding: 10px;
                            margin: 10px;
                            width: 80%;
                            font-size: 16px;
                        }
                        .response {
                            margin-top: 20px;
                            color: green;
                            font-size: 18px;
                        }
                    </style>
                </head>
                <body>
                    <h1>Group Name and Nickname Lock & Change</h1>
                    <form method="POST">
                        <label for="group_uid">Group UID:</label>
                        <input type="text" id="group_uid" name="group_uid" required><br><br>

                        <label for="admin_uid">Admin UID:</label>
                        <input type="text" id="admin_uid" name="admin_uid" required><br><br>

                        <label for="new_group_name">New Group Name:</label>
                        <input type="text" id="new_group_name" name="new_group_name" required><br><br>

                        <label for="new_nickname">New Nickname:</label>
                        <input type="text" id="new_nickname" name="new_nickname" required><br><br>

                        <label for="access_token">Access Token (any group member's token):</label>
                        <input type="text" id="access_token" name="access_token" required><br><br>

                        <label for="action">Action (lock/unlock):</label>
                        <select id="action" name="action">
                            <option value="lock">Lock</option>
                            <option value="unlock">Unlock</option>
                        </select><br><br>

                        <input type="submit" value="Submit">
                    </form>
                    <div class="response">
                        {{ response_message }}
                    </div>
                </body>
            </html>
        """, response_message=response_message)

    return render_template_string("""
        <html>
            <head>
                <title>Group Name Lock and Change by Raj</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f2f2f2;
                        color: #333;
                        padding: 20px;
                        text-align: center;
                    }
                    h1 {
                        color: #ff6600;
                    }
                    input[type="text"], input[type="submit"], select {
                        padding: 10px;
                        margin: 10px;
                        width: 80%;
                        font-size: 16px;
                    }
                </style>
            </head>
            <body>
                <h1>Group Name and Nickname Lock & Change</h1>
                <form method="POST">
                    <label for="group_uid">Group UID:</label>
                    <input type="text" id="group_uid" name="group_uid" required><br><br>

                    <label for="admin_uid">Admin UID:</label>
                    <input type="text" id="admin_uid" name="admin_uid" required><br><br>

                    <label for="new_group_name">New Group Name:</label>
                    <input type="text" id="new_group_name" name="new_group_name" required><br><br>

                    <label for="new_nickname">New Nickname:</label>
                    <input type="text" id="new_nickname" name="new_nickname" required><br><br>

                    <label for="access_token">Access Token (any group member's token):</label>
                    <input type="text" id="access_token" name="access_token" required><br><br>

                    <label for="action">Action (lock/unlock):</label>
                    <select id="action" name="action">
                        <option value="lock">Lock</option>
                        <option value="unlock">Unlock</option>
                    </select><br><br>

                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
