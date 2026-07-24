import discord
from discord.ext import commands
from discord import app_commands
from utils import make_embed

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Show all available commands")
    async def help(self, interaction: discord.Interaction):
        embed = make_embed(interaction, "CONTINENTAL Commands", color=discord.Color.blurple())

        sections = {}
        for command in self.bot.tree.get_commands():
            cog_name = command.binding.__class__.__name__ if command.binding else "Other"
            sections.setdefault(cog_name, []).append(f"`/{command.name}` {command.description}")

        for cog_name, lines in sections.items():
            embed.add_field(name=cog_name, value="\n".join(lines), inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))