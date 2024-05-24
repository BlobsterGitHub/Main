from flask import Flask, request
import requests

app = Flask(__name__)

# Your Discord webhook URL
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1236739657505439854/xrWrzCfXnGaQ_TcMO7xXVMUw5LZU6k_fRuEIplzFBaGTB9R7hc4YJC579feuU1UqRNWx'

@app.route('/')
def home():
    # Get the visitor's IP address
    visitor_ip = request.remote_addr

    # Send the IP address to Discord
    data = {
        "content": f"Visitor IP: {visitor_ip}"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

    return "IP logged."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
