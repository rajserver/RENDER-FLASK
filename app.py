import time
import random
import string
import requests
import undetected_chromedriver as uc
from flask import Flask, Response
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)

# 🟢 Step 1: Random Email Generate using 1secmail API
def generate_email():
    domain = "1secmail.com"
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"{username}@{domain}"
    return username, email

# 🟢 Step 2: Fetch OTP from 1secmail
def get_otp(username):
    inbox_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain=1secmail.com"
    for _ in range(10):  # Try fetching OTP for 10 seconds
        time.sleep(2)
        messages = requests.get(inbox_url).json()
        if messages:
            mail_id = messages[0]['id']
            mail_content_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain=1secmail.com&id={mail_id}"
            mail_content = requests.get(mail_content_url).json()
            return mail_content['body']
    return None

# 🟢 Step 3: Create Facebook Account
def create_facebook_account():
    username, email = generate_email()
    password = "Test@1234"
    first_name = "Raj"
    last_name = "Mishra"

    # Start Headless Chrome
    options = uc.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get("https://www.facebook.com/")

    try:
        # Fill Signup Form
        driver.find_element(By.NAME, "firstname").send_keys(first_name)
        driver.find_element(By.NAME, "lastname").send_keys(last_name)
        driver.find_element(By.NAME, "reg_email__").send_keys(email)
        driver.find_element(By.NAME, "reg_passwd__").send_keys(password)

        # Select Random Birth Date
        driver.find_element(By.ID, "day").send_keys("1")
        driver.find_element(By.ID, "month").send_keys("Jan")
        driver.find_element(By.ID, "year").send_keys("2000")

        # Select Gender
        driver.find_element(By.XPATH, "//input[@value='2']").click()  # Male

        # Submit Form
        driver.find_element(By.NAME, "websubmit").click()

        time.sleep(5)  # Wait for OTP Page

        # Fetch OTP
        otp_body = get_otp(username)
        if otp_body:
            otp_code = "".join(filter(str.isdigit, otp_body))  # Extract OTP
            driver.find_element(By.NAME, "code").send_keys(otp_code + Keys.ENTER)
            time.sleep(3)
            return f"✅ Account Created!<br>Email: {email}<br>Password: {password}"
        else:
            return "❌ OTP Fetch Failed!"

    except Exception as e:
        return f"❌ Error: {str(e)}"

    finally:
        driver.quit()

@app.route("/")
def home():
    return Response('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Account Creator</title>
        <style>
            body { text-align: center; font-family: Arial, sans-serif; margin-top: 100px; }
            button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
            #result { margin-top: 20px; font-size: 18px; color: green; }
        </style>
    </head>
    <body>
        <h1>Facebook Auto Account Creator</h1>
        <button onclick="createAccount()">Create Account</button>
        <div id="result"></div>

        <script>
            function createAccount() {
                document.getElementById("result").innerHTML = "Creating account...";
                fetch('/create')
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById("result").innerHTML = data;
                    });
            }
        </script>
    </body>
    </html>
    ''', mimetype='text/html')

@app.route("/create", methods=["GET"])
def create_account():
    return create_facebook_account()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
