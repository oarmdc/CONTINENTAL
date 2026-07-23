# CONTINENTAL

A Discord bot built with Python and [discord.py](https://github.com/Rapptz/discord.py), featuring music playback powered by a self-hosted [Lavalink](https://github.com/lavalink-devs/Lavalink) server. All commands are slash commands.

## Features

- 🎵 **Music playback** — SoundCloud search, Spotify links, and direct YouTube links (via Lavalink + LavaSrc)
- 📜 **Queue system** — queue up multiple songs, auto-plays the next one when a track ends
- 🆙 **Levels System** — members gain XP by chatting and level up over time
- 🔫 **Snipe** — recover recently deleted or edited messages
- 👋 **Welcome & leave messages**
- 📊 **Dynamic presence** showing server count

## Commands

| Command                    | Description                                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `/play <song name / URL>`  | Plays a song, or adds it to the queue if something is already playing. Joins your voice channel automatically. |
| `/skip`                    | Skips the current song and plays the next one in queue.                                                        |
| `/queue`                   | Shows the current song queue.                                                                                  |
| `/stop`                    | Stops playback and clears the queue.                                                                           |
| `/leave`                   | Disconnects the bot from the voice channel.                                                                    |
| `/snipe`                   | Shows the last deleted message in the channel.                                                                 |
| `/editsnipe`               | Shows the last edited message in the channel (before & after).                                                 |
| `/pfp [member: optional]`            | Shows a member's avatar. Leave empty for your own.                                                             |
| `/rank [member: optional]`| Shows a member's level and XP. Leave empty for your own.                                                       |
| `/leaderboard`             | Shows the top 10 members with the highest levels.                                                              |

## Tech Stack

- **Python 3.12** with [discord.py](https://github.com/Rapptz/discord.py)
- **[Wavelink](https://github.com/PythonistaGuild/Wavelink)** — Lavalink client for discord.py
- **[Lavalink v4](https://github.com/lavalink-devs/Lavalink)** — audio server (self-hosted on a VPS)
  - **SoundCloud** as the primary audio source
  - [LavaSrc](https://github.com/topi314/LavaSrc) plugin — Spotify links resolved through SoundCloud
- **python-dotenv** for configuration
- **aiosqlite** — persistent storage for the leveling system

## Project Structure

```
CONTINENTAL/
├── bot.py               # Connection logic, cog loading, Lavalink node setup
├── utils.py             # Shared helpers (embeds)
├── requirements.txt
└── cogs/
    ├── mainCommands.py  # General commands
    ├── music.py         # Music commands
    ├── events.py        # Event listeners
    ├── adminCommands.py # Moderation commands
    ├── levels.py        # XP and leveling system
    └── snipe.py         # Snipe commands (deleted/edited messages)
```

## Setup

### 1. Clone and install

```
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

This bot requires a running **Lavalink v4** server with SoundCloud enabled and the `LavaSrc` plugin for Spotify support. See the [Lavalink docs](https://lavalink.dev/) for hosting instructions.

### 4. Run

```
python bot.py
```

## Credits

Developed by **oarm** and **camarovx**. Built as a learning project — from `yt-dlp` beginnings to a self-hosted Lavalink server.
