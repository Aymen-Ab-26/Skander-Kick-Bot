from flask import Flask
import os
import requests

app = Flask(__name__)

# Get from Railway Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
TARGET_USER_ID = os.getenv("TARGET_USER_ID")

HEADERS = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/disconnect")
def disconnect_user():
    if not all([BOT_TOKEN, GUILD_ID, TARGET_USER_ID]):
        return "Error: Missing environment variables!", 500
    
    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{TARGET_USER_ID}"
    
    try:
        response = requests.patch(url, headers=HEADERS, json={"channel_id": None}, timeout=10)
        
        if response.ok:
            return "✅ User disconnected successfully!", 200
        else:
            return f"❌ Failed: {response.status_code} - {response.text}", response.status_code
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/")
def home():
    return """
    <h1>Discord Disconnect Bot ✅</h1>
    <p><a href="/disconnect">Click here to disconnect the user</a></p>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))   # Railway uses 8080
    app.run(host="0.0.0.0", port=port)
