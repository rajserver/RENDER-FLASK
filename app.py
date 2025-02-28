from flask import Flask, render_template_string

app = Flask(__name__)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Facebook Login & Sign Up Clone</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f0f2f5;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 1000px;
      margin: 40px auto;
      display: flex;
      justify-content: space-between;
      padding: 0 20px;
    }
    .login-section {
      flex: 1;
      padding: 20px;
    }
    .login-section h1 {
      color: #1877f2;
      font-size: 50px;
      margin-bottom: 20px;
    }
    .login-form {
      background-color: #fff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .login-form input {
      width: 100%;
      padding: 12px;
      margin: 8px 0;
      border: 1px solid #ddd;
      border-radius: 4px;
    }
    .login-form button {
      width: 100%;
      background-color: #1877f2;
      color: #fff;
      padding: 12px;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      margin-top: 10px;
      cursor: pointer;
    }
    .signup-section {
      flex: 1;
      padding: 20px;
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      margin-left: 20px;
    }
    .signup-section h2 {
      font-size: 24px;
      margin-bottom: 10px;
    }
    .signup-form input {
      width: calc(50% - 10px);
      padding: 10px;
      margin: 5px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }
    .signup-form input.full {
      width: calc(100% - 10px);
    }
    .signup-form button {
      width: 100%;
      background-color: #42b72a;
      color: #fff;
      padding: 12px;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      margin-top: 10px;
      cursor: pointer;
    }
    .note {
      font-size: 12px;
      color: #666;
      margin-top: 10px;
    }
    /* Responsive adjustments */
    @media (max-width: 768px) {
      .container {
        flex-direction: column;
      }
      .signup-section {
        margin-left: 0;
        margin-top: 20px;
      }
      .signup-form input {
        width: calc(100% - 10px);
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Login Section -->
    <div class="login-section">
      <h1>facebook</h1>
      <div class="login-form">
        <form onsubmit="openFacebook('login'); return false;">
          <input type="text" name="email" placeholder="Email or phone number" required>
          <input type="password" name="pass" placeholder="Password" required>
          <button type="submit">Log In</button>
        </form>
      </div>
      <p class="note">Note: Clicking Log In will open Facebook’s login page in a new tab.</p>
    </div>
    <!-- Sign Up Section -->
    <div class="signup-section">
      <h2>Create a New Account</h2>
      <form onsubmit="openFacebook('signup'); return false;" class="signup-form">
        <input type="text" name="firstname" placeholder="First name" required>
        <input type="text" name="lastname" placeholder="Last name" required>
        <input type="text" name="reg_email__" placeholder="Mobile number or email" class="full" required>
        <input type="password" name="reg_passwd__" placeholder="New password" class="full" required>
        <!-- For simplicity, birthday and gender fields are omitted -->
        <button type="submit">Sign Up</button>
      </form>
      <p class="note">Note: Clicking Sign Up will open Facebook’s sign up page in a new tab.</p>
    </div>
  </div>
  <script>
    function openFacebook(type) {
      if (type === 'login') {
        window.open("https://m.facebook.com/login", "_blank");
      } else if (type === 'signup') {
        window.open("https://m.facebook.com/r.php", "_blank");
      }
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_content)

if __name__ == '__main__':
    # Deploy on host 0.0.0.0 and port 5000 (change port if needed)
    app.run(host="0.0.0.0", port=5000, debug=True)
