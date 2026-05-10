// disconnect-bot.js
const http = require("http");

const BOT_TOKEN = "MTUwMzAwOTQ3MTg2NDExMTExNA.GmLA-M.vodee5W-LcRY89d44S_WQCLsyr48t47oPH7Dt4";
const GUILD_ID = "1437390219237392387";       // Right-click server → Copy ID
const TARGET_USER_ID = "597767820192776205"; // The person's user ID

http.createServer(async (req, res) => {
  if (req.url === "/disconnect") {
    // Patch the user's voice state to channel: null = disconnect
    const response = await fetch(
      `https://discord.com/api/v10/guilds/${GUILD_ID}/members/${TARGET_USER_ID}`,
      {
        method: "PATCH",
        headers: {
          Authorization: `Bot ${BOT_TOKEN}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ channel_id: null }),
      }
    );
    res.end(response.ok ? "Disconnected!" : "Failed: " + response.status);
  } else {
    res.end("OK");
  }
}).listen(9999, () => console.log("Listening on port 9999"));