from flask import Flask
from threading import Thread
import requests
import time

app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def ping_server():
    # Replace with your actual live app URL on Render
    url = "https://rmf-helper-bot.onrender.com"
    while True:
        time.sleep(240)  # Waits 4 minutes between pings
        try:
            response = requests.get(url)
            print(f"Self-ping successful: Status {response.status_code}")
        except Exception as e:
            print(f"Self-ping failed: {e}")

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # Start the Flask server thread
    t = Thread(target=run)
    t.daemon = True
    t.start()

    # Start the background self-ping thread
    ping_thread = Thread(target=ping_server)
    ping_thread.daemon = True
    ping_thread.start()
