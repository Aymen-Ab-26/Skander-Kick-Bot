from flask import Flask
import os
import requests
import threading
import asyncio
import discord

app = Flask(__name__)

# Railway Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
TARGET_USER_ID = os.getenv("TARGET_USER_ID")

# ============== FLASK WEB PART ==============
@app.route("/")
def home():
    return """
    <h1>✅ Discord Disconnect Bot</h1>
    <p><strong>Bot Status:</strong> 🟢 Online</p>
    <br>
    <a href="/disconnect" style="font-size:28px; padding:20px 30px; background:#7289da; color:white; text-decoration:none; border-radius:10px;">
        🔌 Disconnect User Now
    </a>
    """

@app.route("/disconnect")
def disconnect_user():
    if not all([BOT_TOKEN, GUILD_ID, TARGET_USER_ID]):
        return "❌ Missing environment variables!", 500

    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{TARGET_USER_ID}"
    
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(url, headers=headers, json={"channel_id": None}, timeout=10)
        if response.ok:
            return "✅ User disconnected successfully!", 200
        else:
            return f"❌ Failed: {response.status_code}<br>{response.text}", response.status_code
    except Exception as e:
        return f"❌ Error: {str(e)}", 500


# ============== DISCORD BOT PART (Shows Online) ==============
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is now ONLINE as {bot.user}")
    guild = bot.get_guild(int(GUILD_ID))
    if guild:
        print(f"✅ Connected to server: {guild.name}")
    else:
        print("⚠️ Could not find server with that GUILD_ID")

# Run Discord Bot
async def run_discord_bot():
    await bot.start(BOT_TOKEN)

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_discord_bot())

# Start bot in background thread
threading.Thread(target=start_bot, daemon=True).start()

# ============== START FLASK ==============
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print("🚀 Starting Flask + Discord Bot...")
    app.run(host="0.0.0.0", port=port)
