import discord
from discord import app_commands
from discord.ext import commands
from utils import make_embed

class mainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(description= "Get an avatar. Leave empty for your own, or mention someone to get theirs.")
    async def pfp(self, interaction: discord.Interaction, thatuser: discord.Member = None):
        target = thatuser or interaction.user
        embed = make_embed(interaction, f"{target.name}'s avatar", image=target.display_avatar.url, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(mainCommands(bot))