# CONTINENTAL

A Discord bot built with Python and discord.py, made by oarm and camarovx as a side project to learn the ropes of bot development, slash commands, and self-hosted infrastructure. Started as a simple music bot with prefix commands, and has since grown into something a lot more complete.

## What it does

**Music** — Plays songs from SoundCloud, YouTube, and Spotify (via a self-hosted Lavalink server), with a queue system and automatic retry logic when a track fails to load.

**Leveling** — Members earn XP by chatting, with a cooldown to prevent spam. Check your progress with `/rank` or see who's on top with `/leaderboard`.

**Economy** — A fake currency system for fun. Claim daily rewards, send money to other members, or top up balances if you're an admin. Balances are shared across every server the bot is in, and you can choose to keep yours private.

**Birthdays** — Save your birthday and get a DM from the bot when the day comes around.

**Snipe** — Recover recently deleted or edited messages in a channel.

**Moderation** — Basic ban and kick commands for admins.

**Valorant stats** — Look up a player's current rank, peak rank, and account details straight from Discord.

Run `/help` in any server the bot is in to see the full, always-up-to-date list of commands.

## Tech stack

- Python 3.12, discord.py (slash commands via app_commands)
- Wavelink as the Lavalink client
- Lavalink v4, self-hosted on an Azure VM, with the youtube-source and LavaSrc plugins
- aiosqlite for persistent storage (levels, birthdays, economy)
- python-dotenv for configuration

## Project structure

```
CONTINENTAL/
├── bot.py               # Bot setup, cog loading, Lavalink connection
├── utils.py              # Shared embed helpers
├── requirements.txt
└── cogs/
    ├── mainCommands.py   # Profile pictures, birthdays
    ├── music.py          # Music playback and queue
    ├── levels.py         # XP and leveling
    ├── money.py          # Economy system
    ├── adminCommands.py  # Moderation
    ├── snipe.py          # Message recovery
    ├── valorant.py        # Valorant stats lookup
    ├── help.py            # Auto-generated help command
    └── events.py          # Welcome/leave messages, presence updates
```

## Setup

### 1. Clone and install

```
git clone https://github.com/oarmdc/CONTINENTAL.git
cd CONTINENTAL
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```
DISCORD_TOKEN=your_discord_bot_token
LAVALINK_HOST=your_lavalink_server_ip
LAVALINK_PASSWORD=your_lavalink_password
HENRIK_API_KEY=your_henrikdev_api_key
```

Never commit this file. It's already listed in `.gitignore`.

### 3. Lavalink server

You'll need a running Lavalink v4 server with the youtube-source and LavaSrc plugins installed. See the [Lavalink docs](https://lavalink.dev/) for setup instructions.

### 4. Run

```
python bot.py
```

## Credits

Built by oarm and camarovx, as a learning project that's grown well past its original scope.