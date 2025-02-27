from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to get linked Facebook accounts
def get_facebook_accounts(user_input):
    try:
        search_url = f"https://www.facebook.com/login/identify/?ctx=recover&search_attempts=1&alternate_search=1&email={user_input}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36"
        }
        
        session = requests.Session()
        response = session.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        accounts = []
        for div in soup.find_all("div", class_="pam"):
            name = div.find("strong")
            profile_link = div.find("a")
            if name and profile_link and "href" in profile_link.attrs:
                profile_url = "https://www.facebook.com" + profile_link["href"]
                accounts.append({"name": name.text, "profile_url": profile_url})
        
        return accounts
    except:
        return []

# Flask Route
@app.route("/", methods=["GET", "POST"])
def index():
    result_html = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        accounts = get_facebook_accounts(user_input)

        if accounts:
            result_html += "<h3>Linked Accounts Found:</h3><ul>"
            for acc in accounts:
                result_html += f'<li><strong>{acc["name"]}</strong> - <a href="{acc["profile_url"]}" target="_blank">View Profile</a></li>'
            result_html += "</ul>"
        else:
            result_html = "<h3>No linked accounts found.</h3>"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FB ID Finder</title>
    </head>
    <body>
        <h2>Find Facebook IDs Linked to Your Email/Phone</h2>
        <form method="post">
            <input type="text" name="user_input" placeholder="Enter Email or Phone" required>
            <button type="submit">Find Accounts</button>
        </form>
        {result_html}
    </body>
    </html>
    """

# Run Flask App on Mobile
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
