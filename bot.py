import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="leo.", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name=f"with {len(bot.guilds)} Servers."))

async def main():
    async with bot:
        await bot.load_extension("cogs.mainCommands")
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())