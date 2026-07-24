import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv
import wavelink
import aiosqlite

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

@bot.event
async def on_wavelink_node_ready(payload: wavelink.NodeReadyEventPayload):
    print(f"Lavalink node ready: {payload.node.identifier}")

@bot.event
async def setup_hook():
    bot.db = await aiosqlite.connect("database.db")
    await bot.load_extension("cogs.mainCommands")
    await bot.load_extension("cogs.music")
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.snipe")
    await bot.load_extension("cogs.adminCommands")
    await bot.load_extension("cogs.levels")
    await bot.load_extension("cogs.valorant")
    await bot.load_extension("cogs.money")
    await bot.tree.sync()
    node = wavelink.Node(uri=f"http://{os.getenv('LAVALINK_HOST')}:2333", password=os.getenv("LAVALINK_PASSWORD"))
    await wavelink.Pool.connect(nodes=[node], client=bot)

async def main():
    try:
        async with bot:
            await bot.start(os.getenv("DISCORD_TOKEN"))
    finally:
        if getattr(bot, "db", None):
            await bot.db.close()

asyncio.run(main())