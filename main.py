from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

BOT_TOKEN = "MTUwMzAwOTQ3MTg2NDExMTExNA.GmLA-M.vodee5W-LcRY89d44S_WQCLsyr48t47oPH7Dt4"
GUILD_ID = "1437390219237392387"
TARGET_USER_ID = "597767820192776205"

HEADERS = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}


@app.route("/disconnect")
def disconnect_user():
    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{TARGET_USER_ID}"
    
    payload = {"channel_id": None}
    
    response = requests.patch(url, headers=HEADERS, json=payload)
    
    if response.ok:
        return "Disconnected!", 200
    else:
        return f"Failed: {response.status_code} - {response.text}", response.status_code


@app.route("/")
def home():
    return "Discord Disconnect Bot is running ✅"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9999))
    app.run(host="0.0.0.0", port=port)
