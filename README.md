# 🦖 TranqBot — A Discord Community Moderation Bot

**TranqBot** is a fun, community-driven moderation tool for Discord servers. Inspired by dinosaur survival themes, it allows members to react to disruptive messages with a tranquilizer emoji. If a message reaches a configured number of tranq reactions, the author is "tranquilized" — temporarily muted with a special role and unable to speak for a set duration.

---

## ✨ Features

- 💤 **Community moderation**: A role is applied after a threshold of emoji reactions  
- ⏱ **Temporary mute**: The role is removed after a configurable time (e.g., 30 minutes)  
- 🤖 **Bot retaliation**: If someone tries to tranquilize the bot, they get muted instead — with snarky commentary  
- 🔁 **Startup cleanup**: Removes leftover muted roles on reboot  
- 📜 **Auto permission override**: Restricts muted users from sending messages in all categories  
- 🔗 **Admin logging**: Logs all tranquilizations to a configured log channel with clickable jump-to-message links  
- 🍗 **Taming flavor**: Users can react with a "kibble" emoji to get fun taming messages  

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tranqbot.git
cd tranqbot
```

### 2. Create a `.env` Configuration File

In the root of the project, create a `.env` file and populate it like this:

```env
DISCORD_TOKEN=your_bot_token_here
SERVER_ID=your_discord_server_id
ADMIN_LOG_CHANNEL_ID=channel_id_for_logs

TRANQ_EMOJI_NAME=tranq_dart
KIBBLE_EMOJI_NAME=kibble
TRANQ_ROLE_NAME=Tranq'ed

REACTION_THRESHOLD=5
SLEEP_DURATION=1800  # in seconds (e.g. 1800 = 30 minutes)
```

> 💡 Emoji names must match exactly what appears in your server’s emoji list (e.g., `tranq_dart`, not `:<123456>`).

---

### 3. Install Dependencies

Use `pip` to install required libraries:

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**

```
discord.py>=2.3.2
python-dotenv>=1.0.0
```

---

### 4. Run the Bot

Start the bot using:

```bash
python TranqBot.py
```
ALternatively, you can use the included Launch_TranqBot.bat file.

---

## 🛡 Role and Permission Setup

### ✅ Bot Role

Your bot must have the following permissions:
- `Manage Roles`
- `Read Message History`
- `Read Messages / View Channels`
- `Send Messages`
- `Add Reactions`

### ✅ "Tranq'ed" Role

Create a role named exactly as `TRANQ_ROLE_NAME` in your `.env`. Then:

- Place it **below the bot's role** in the server's role hierarchy  
- Disable the following permissions:
  - Send Messages
  - Send Messages in Threads
  - Create Public Threads
  - Create Private Threads  
- Keep `Add Reactions` **enabled** so they can still interact  

> The bot will automatically apply these restrictions across all categories when it starts.

---

## 🧪 Testing It Out

1. Add a custom emoji to your server named `tranq_dart`  
2. Post a test message  
3. React to it with `:tranq_dart:` — once the threshold is met, the author is muted  
4. Try reacting with `:kibble:` during their nap for flavor text  
5. Try tranqing the bot — enjoy the punishment 😏
