from flask import Flask, render_template_string, request

app = Flask(__name__)

# Simulated database for group and admin data
groups_db = {
    "group1_uid": {
        "name": "Original Group Name",
        "nickname": "Original Nickname",
        "locked": True,
        "admin_uid": "admin_uid_1"
    }
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        group_uid = request.form['group_uid']
        admin_uid = request.form['admin_uid']
        new_name = request.form['new_name']
        new_nickname = request.form['new_nickname']
        action = request.form['action']

        # Check if group exists
        if group_uid not in groups_db:
            return "Group UID not found!"

        group = groups_db[group_uid]

        # Check if the admin UID matches
        if admin_uid != group["admin_uid"]:
            return "You are not authorized to change this group!"

        if action == 'lock':
            # Lock the group name and nickname
            group['name'] = new_name
            group['nickname'] = new_nickname
            group['locked'] = True
            return f"Group name and nickname locked as '{new_name}' and '{new_nickname}'."

        elif action == 'unlock':
            # Unlock the group name and nickname
            group['locked'] = False
            return f"Group {group_uid} is now unlocked, and name/nickname can be changed freely."

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Group Name Lock BY RAJ</title>
    <style>
        body {
            background: #333;
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;
            animation: fadeIn 5s ease-in-out infinite;
        }
        h1, h2 {
            font-size: 2.5em;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
        }
        @keyframes fadeIn {
            0% { background-color: #111; }
            50% { background-color: #444; }
            100% { background-color: #111; }
        }
        form {
            margin-top: 20px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
        }
        input, select {
            margin: 10px;
            padding: 10px;
            width: 300px;
            border-radius: 5px;
            border: none;
        }
        input[type="submit"] {
            background-color: #f44336;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #d32f2f;
        }
    </style>
</head>
<body>
    <h1>Group Name Lock System</h1>
    <h2>By RAJ</h2>
    <form method="POST">
        <label for="group_uid">Group UID:</label>
        <input type="text" id="group_uid" name="group_uid" required><br><br>

        <label for="admin_uid">Admin UID:</label>
        <input type="text" id="admin_uid" name="admin_uid" required><br><br>

        <label for="new_name">New Group Name:</label>
        <input type="text" id="new_name" name="new_name" required><br><br>

        <label for="new_nickname">New Nickname:</label>
        <input type="text" id="new_nickname" name="new_nickname" required><br><br>

        <label for="action">Action:</label>
        <select name="action" id="action">
            <option value="lock">Lock Group Name & Nickname</option>
            <option value="unlock">Unlock Group Name & Nickname</option>
        </select><br><br>

        <input type="submit" value="Submit">
    </form>
    <footer style="position: fixed; bottom: 10px; width: 100%; text-align: center;">
        <p>VAMPIRE RULEX BOY RAJ MISHRA</p>
    </footer>
</body>
</html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
