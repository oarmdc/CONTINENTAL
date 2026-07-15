import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone
from utils import make_embed, send_error_embed


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages = {}
        self.edited_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        # Don't snipe a command invocation that events.py auto-deletes
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return
        if not message.content and not message.attachments:
            return

        self.deleted_messages[message.channel.id] = {
            "content": message.content or "*[no text content]*",
            "author": message.author,
            "avatar": message.author.display_avatar.url,
            "timestamp": datetime.now(timezone.utc),
            "attachment": message.attachments[0].url if message.attachments else None,
        }

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.content == after.content:
            return

        self.edited_messages[before.channel.id] = {
            "before": before.content or "*[no text content]*",
            "after": after.content or "*[no text content]*",
            "author": before.author,
            "avatar": before.author.display_avatar.url,
            "timestamp": datetime.now(timezone.utc),
        }

    @app_commands.command()
    async def snipe(self, interaction: discord.Interaction):
        data = self.deleted_messages.get(interaction.channel.id)
        if data is None:
            await send_error_embed(interaction, "There's nothing to snipe in this channel.")
            return

        embed = make_embed(
            interaction,
            f"🔫 Sniped Message of {data['author'].display_name}",
            description=data["content"],
            color=discord.Color.orange(),
            timestamp=data["timestamp"],
            image=data["attachment"],
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def editsnipe(self, interaction: discord.Interaction):
        data = self.edited_messages.get(interaction.channel.id)
        if data is None:
            await send_error_embed(interaction, "There's nothing to editsnipe in this channel.")
            return

        embed = make_embed(
            interaction,
            f"✏️ Edited Message of {data['author'].display_name}",
            color=discord.Color.orange(),
            timestamp=data["timestamp"],
        )
        embed.add_field(name="Before", value=data["before"], inline=False)
        embed.add_field(name="After", value=data["after"], inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Snipe(bot))