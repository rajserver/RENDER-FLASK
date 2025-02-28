from flask import Flask, render_template_string

app = Flask(__name__)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Facebook Lite Clone</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      text-align: center;
      font-family: Arial, sans-serif;
      background-color: #f0f0f0;
      color: #333;
      transition: background-color 0.3s, color 0.3s;
    }
    .dark-mode {
      background-color: #121212;
      color: #ddd;
    }
    header {
      padding: 10px 20px;
      background-color: #4267B2;
      color: white;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    header.dark-mode {
      background-color: #1b1b1b;
    }
    .tabs {
      display: flex;
      justify-content: center;
      background-color: #ddd;
    }
    .tabs button {
      background-color: inherit;
      border: none;
      outline: none;
      padding: 10px 20px;
      cursor: pointer;
      transition: background-color 0.3s;
      font-size: 16px;
    }
    .tabs button:hover {
      background-color: #bbb;
    }
    .tabs button.active {
      background-color: #ccc;
      font-weight: bold;
    }
    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
    }
    .fb-btn {
      display: block;
      width: 200px;
      margin: 20px auto;
      padding: 10px;
      background-color: #4267B2;
      color: white;
      text-align: center;
      text-decoration: none;
      border-radius: 5px;
      font-size: 18px;
    }
    .fb-btn:hover {
      background-color: #365899;
    }
    .toggle-btn {
      background-color: #fff;
      color: #333;
      border: none;
      padding: 5px 10px;
      cursor: pointer;
      border-radius: 5px;
    }
  </style>
</head>
<body>
  <header id="header">
    <h1>Facebook Lite Clone</h1>
    <button class="toggle-btn" onclick="toggleDarkMode()">Toggle Dark Mode</button>
  </header>
  <div class="tabs">
    <button class="tablink active" onclick="openTab(event, 'tab1')">Account 1</button>
    <button class="tablink" onclick="openTab(event, 'tab2')">Account 2</button>
  </div>
  <div id="tab1" class="tab-content active">
    <a class="fb-btn" href="https://m.facebook.com/lite" target="_blank">Open Facebook Lite (Acc 1)</a>
  </div>
  <div id="tab2" class="tab-content">
    <a class="fb-btn" href="https://m.facebook.com/lite" target="_blank">Open Facebook Lite (Acc 2)</a>
  </div>
  <script>
    // Toggle dark mode
    function toggleDarkMode() {
      document.body.classList.toggle('dark-mode');
      document.getElementById('header').classList.toggle('dark-mode');
    }
    // Tab switching
    function openTab(evt, tabName) {
      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tab-content");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
      }
      tablinks = document.getElementsByClassName("tablink");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
      }
      document.getElementById(tabName).classList.add("active");
      evt.currentTarget.classList.add("active");
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
