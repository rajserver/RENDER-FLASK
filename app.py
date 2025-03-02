from flask import Flask, request
import pyautogui
import time
import threading

app = Flask(__name__)

# Global Variables
typing_thread = None
is_typing = False

def auto_typing(text, speed, loop_mode):
    global is_typing
    while is_typing:
        for char in text:
            if not is_typing:
                break
            pyautogui.typewrite(char)
            time.sleep(speed / 1000)
        if not loop_mode:
            break

@app.route('/')
def home():
    return """  
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PF Auto-Typer Clone</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            textarea { width: 300px; height: 100px; }
            input, button { margin: 5px; }
            .container { background: #f9f9f9; padding: 20px; border-radius: 10px; width: 350px; margin: auto; box-shadow: 2px 2px 10px gray; }
        </style>
    </head>
    <body>

        <div class="container">
            <h2>PF Auto-Typer Clone</h2>
            
            <textarea id="textInput" placeholder="Enter text here..."></textarea><br>

            <label>Typing Speed (ms per character):</label>
            <input type="number" id="typingSpeed" value="50"><br>

            <label>Start Delay (ms):</label>
            <input type="number" id="startDelay" value="0"><br>

            <label>Loop Mode:</label>
            <input type="checkbox" id="loopMode"><br>

            <button onclick="startTyping()">Start</button>
            <button onclick="stopTyping()">Stop</button>
        </div>

        <script>
            function startTyping() {
                let text = document.getElementById("textInput").value;
                let speed = document.getElementById("typingSpeed").value;
                let delay = document.getElementById("startDelay").value;
                let loopMode = document.getElementById("loopMode").checked;
                
                fetch("/start", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: text, speed: speed, delay: delay, loopMode: loopMode })
                }).then(response => response.json())
                  .then(data => alert(data.status));
            }

            function stopTyping() {
                fetch("/stop", { method: "POST" })
                    .then(response => response.json())
                    .then(data => alert(data.status));
            }
        </script>

    </body>
    </html>
    """

@app.route('/start', methods=['POST'])
def start_typing():
    global typing_thread, is_typing
    if is_typing:
        return {"status": "Already Typing!"}
    
    data = request.json
    text = data.get("text", "")
    speed = int(data.get("speed", 50))
    delay = int(data.get("delay", 0))
    loop_mode = data.get("loopMode", False)

    time.sleep(delay / 1000)  # Start delay
    is_typing = True
    typing_thread = threading.Thread(target=auto_typing, args=(text, speed, loop_mode))
    typing_thread.start()
    
    return {"status": "Typing Started!"}

@app.route('/stop', methods=['POST'])
def stop_typing():
    global is_typing
    is_typing = False
    return {"status": "Typing Stopped!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
