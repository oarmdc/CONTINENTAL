import discord
from discord.ext import commands
from utils import update_presence

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_guild_remove")
    @commands.Cog.listener("on_guild_join")
    async def on_guild_change(self, guild):
        await update_presence(self.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"Welcome {member.mention} !")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"Sad to see you leave {member} !")

async def setup(bot):
    await bot.add_cog(Events(bot))