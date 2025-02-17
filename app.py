from flask import Flask, request, render_template_string, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pickle

app = Flask(__name__)

# Initialize WebDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Facebook login function to extract cookies
def facebook_login(email, password):
    driver = get_driver()
    driver.get("https://www.facebook.com/login")
    
    # Enter credentials
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "pass")
    email_field.send_keys(email)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    
    sleep(5)  # Wait for login to complete

    # Check for successful login
    try:
        driver.find_element(By.XPATH, "//div[@aria-label='Account']")
        print("Login Successful!")
    except Exception as e:
        print("Login failed:", e)
        driver.quit()
        return None

    # Extract cookies after login
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

# Save cookies to a file
def save_cookies(cookies, filename="cookies.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(cookies, file)

# Load cookies from file
def load_cookies(filename="cookies.pkl"):
    try:
        with open(filename, "rb") as file:
            cookies = pickle.load(file)
        return cookies
    except FileNotFoundError:
        return None

# Home route to show the form
@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Cookies Extractor</title>
        </head>
        <body>
            <h2>Facebook Cookies Extractor</h2>
            <form action="/extract_cookies" method="POST">
                <label for="email">Facebook Email:</label>
                <input type="text" id="email" name="email" required><br><br>
                <label for="password">Facebook Password:</label>
                <input type="password" id="password" name="password" required><br><br>
                <button type="submit">Extract Cookies</button>
            </form>

            <h3>Check Cookies</h3>
            <button onclick="window.location.href='/check_cookies'">Check Current Cookies</button>
        </body>
        </html>
    ''')

# Route to extract cookies
@app.route('/extract_cookies', methods=['POST'])
def extract_cookies():
    email = request.form['email']
    password = request.form['password']
    
    cookies = facebook_login(email, password)
    
    if cookies:
        save_cookies(cookies)
        return jsonify({"status": "success", "message": "Cookies extracted successfully!"})
    else:
        return jsonify({"status": "error", "message": "Login failed. Please check credentials."})

# Route to check current session cookies
@app.route('/check_cookies')
def check_cookies():
    cookies = load_cookies()
    if cookies:
        return jsonify({"status": "success", "message": "Cookies found!", "cookies": cookies})
    else:
        return jsonify({"status": "error", "message": "No cookies found."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
