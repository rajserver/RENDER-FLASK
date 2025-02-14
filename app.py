from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        group_uid = request.form["group_uid"]
        admin_uid = request.form["admin_uid"]
        new_group_name = request.form["new_group_name"]
        new_nickname = request.form["new_nickname"]
        
        # Simulate the group name and nickname change
        # Here, normally you would use API calls to Facebook/Instagram to change the name, but we'll just return a success message.
        response_message = f"Group name and nickname have been successfully updated to '{new_group_name}' and '{new_nickname}', and they are now locked."

        # Return the response
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
                        input[type="text"], input[type="submit"] {
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
                    input[type="text"], input[type="submit"] {
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

                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    """)

if __name__ == "__main__":
    # Running Flask app with host and port defined
    app.run(host='0.0.0.0', port=5000)
