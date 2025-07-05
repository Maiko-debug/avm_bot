# AVM Bot 🤖

> **All VIP Members Bot** — A Discord moderation + community management bot for private and public servers.

### 💡 Features

- 🔧 Admin tools (`!mute`, `!ban`, `!purge`, `/setmodlog`)
- ⚠️ Auto-moderation (triggers: spam, n-word, caps, etc.)
- 💬 Welcome system (customizable)
- 🎨 Embed builder
- 📋 Reaction roles
- ⚙️ Slash config: `/avmconfig`, `/status`, `/avmhelp`

### 🚀 Getting Started

1. Clone the repo
2. Add a `.env` file with:
```
DISCORD_TOKEN=your-bot-token-here
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the bot:
```
python main.py
```

### 🛠 Built With
- Python 3.11+
- `discord.py` (nextcord/pycord compatible)
- Railway for deployment