# CONTINENTAL

A Discord bot built with Python and [discord.py](https://github.com/Rapptz/discord.py), featuring music playback powered by a self-hosted [Lavalink](https://github.com/lavalink-devs/Lavalink) server.

**Prefix:** `leo.`

## Features

- 🎵 **Music playback** — YouTube links, YouTube search, and Spotify links (via Lavalink + LavaSrc)
- 👋 **Welcome & leave messages**
- 🧹 **Auto-deletes command messages** to keep channels clean
- 📊 **Dynamic presence** showing server count

## Commands

| Command | Description |
|---------|-------------|
| `leo.play <song name / URL>` | Plays a song from YouTube or Spotify. Joins your voice channel automatically. |
| `leo.stop` | Stops the current song. |
| `leo.leave` | Disconnects the bot from the voice channel. |

More commands (queue, pause/resume, skip, tickets) are planned.

## Tech Stack

- **Python 3.12** with [discord.py](https://github.com/Rapptz/discord.py)
- **[Wavelink](https://github.com/PythonistaGuild/Wavelink)** — Lavalink client for discord.py
- **[Lavalink v4](https://github.com/lavalink-devs/Lavalink)** — audio server (self-hosted on a VPS)
  - [youtube-source](https://github.com/lavalink-devs/youtube-source) plugin
  - [LavaSrc](https://github.com/topi314/LavaSrc) plugin for Spotify support
- **python-dotenv** for configuration

## Project Structure

```
CONTINENTAL/
├── bot.py               # Connection logic, cog loading, Lavalink node setup
├── utils.py             # Shared helpers (embeds)
├── requirements.txt
└── cogs/
    ├── mainCommands.py  # General commands
    ├── music.py         # Music commands
    └── events.py        # Event listeners
```

## Setup

### 1. Clone and install

```bash
git clone https://github.com/oarmdc/CONTINENTAL.git
cd CONTINENTAL
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```
DISCORD_TOKEN=your_discord_bot_token
LAVALINK_HOST=your_lavalink_server_ip
LAVALINK_PASSWORD=your_lavalink_password
```

> ⚠️ Never commit your `.env` file. It's already in `.gitignore`.

### 3. Lavalink server

This bot requires a running **Lavalink v4** server with the `youtube-source` and `LavaSrc` plugins. See the [Lavalink docs](https://lavalink.dev/) for hosting instructions.

### 4. Run

```bash
python bot.py
```

## Credits

Developed by **Omar** and partner. Built as a learning project — from `yt-dlp` beginnings to a self-hosted Lavalink server.
