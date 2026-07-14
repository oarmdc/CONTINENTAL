import discord
from discord.ext import commands
from utils import make_embed, send_error_embed, send_success_embed

class adminCommands(commands.Cog):
    def __init__(self, bot):
        self = bot

    ...

async def setup(bot):
    await bot.add_cog(adminCommands(bot))