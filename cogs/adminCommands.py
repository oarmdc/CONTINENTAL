import discord
from discord import app_commands
from discord.ext import commands
from utils import make_embed, send_error_embed, send_success_embed

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(description="Ban a member from the server")
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if interaction.user.id != interaction.guild.owner_id and member.id == interaction.guild.owner_id:
            await send_error_embed(interaction, "You can't ban the owner, man..")
            return
        if interaction.user.id != interaction.guild.owner_id and member.guild_permissions.administrator:
            await send_error_embed(interaction, "You can't ban another admin.")
            return
        await member.ban(reason=reason)
        await send_success_embed(interaction, f"{member.name} is now banned.")
    @ban.error
    async def ban_error(self, interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await send_error_embed(interaction, "You don't have permission to use this command.")

    @app_commands.command(description="Kick a member from the server")
    @app_commands.checks.has_permissions(administrator=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if interaction.user.id != interaction.guild.owner_id and member.id == interaction.guild.owner_id:
            await send_error_embed(interaction, "You can't kick the owner, man..")
            return
        if interaction.user.id != interaction.guild.owner_id and member.guild_permissions.administrator:
            await send_error_embed(interaction, "You can't kick another admin.")
            return
        await member.kick(reason=reason)
        await send_success_embed(interaction, f"{member.name} is now kicked.")
    @kick.error
    async def kick_error(self, interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await send_error_embed(interaction, "You don't have permission to use this command.")

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))