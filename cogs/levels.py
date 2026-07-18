import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
import time
from utils import make_embed, send_error_embed

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = None
        self.cooldowns = {}

    async def cog_load(self):
        self.db = await aiosqlite.connect("levels.db")
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS levels (
                user_id INTEGER,
                guild_id INTEGER,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, guild_id)
            )
        """)
        await self.db.commit()

    async def cog_unload(self):
        await self.db.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return
        
        now = time.time()
        key = (message.author.id, message.guild.id)
        if message.author.id not in (979460790178443285, 852889536840073247):
            if now - self.cooldowns.get(key, 0) < 60:
                return
            self.cooldowns[key] = now
        await self.db.execute("""
            INSERT INTO levels (user_id, guild_id, xp)
            VALUES (?, ?, 15)
            ON CONFLICT(user_id, guild_id)
            DO UPDATE SET xp = xp + 15
        """, (message.author.id, message.guild.id))

        async with self.db.execute(
            "SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?",
            (message.author.id, message.guild.id)
        ) as cursor:
            row = await cursor.fetchone()
        xp, level = row

        needed = 100 + (level * 50)
        if xp >= needed:
            await self.db.execute(
                "UPDATE levels SET xp = xp - ?, level = level + 1 WHERE user_id = ? AND guild_id = ?",
                (needed, message.author.id, message.guild.id)
            )
            await message.channel.send(
                embed=make_embed(None, f"Level UP! | {message.guild}", description=f"🎉 {message.author.display_name} reached level {level + 1}!", color=discord.Color.gold())
            )

        await self.db.commit()
    
    @app_commands.command(description="Show your level and XP")
    async def rank(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        async with self.db.execute("SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?",
                                   (member.id, interaction.guild.id)
                                   ) as cursor:
            row = await cursor.fetchone()
        if row is None:
            await send_error_embed(interaction, f"{member.display_name} has no XP yet.")
            return
        xp, level = row
        needed = 100 + (level * 50)
        await interaction.response.send_message(
            embed=make_embed(interaction, f"{member.display_name} — Level {level}",
                             description=f"XP: {xp} / {needed}",
                             thumbnail=member.display_avatar.url,
                             color=discord.Color.gold())
        )

    @app_commands.command(description="Show the top 10 users by level")
    async def leaderboard(self, interaction: discord.Interaction):
        async with self.db.execute(
            "SELECT user_id, xp, level FROM levels WHERE guild_id = ? ORDER BY level DESC, xp DESC LIMIT 10",
            (interaction.guild.id, )
        ) as cursor:
            rows = await cursor.fetchall()
        if not rows:
            await send_error_embed(interaction, "Nobody has any XP yet.")
            return
        lines = []
        for i, (user_id, xp, level) in enumerate(rows, start= 1):
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f"Unknown ({user_id})"
            lines.append(f"**{i}** {name} - Level {level} ({xp} XP)")
        await interaction.response.send_message(
            embed=make_embed(interaction, f"Leaderboard | {interaction.guild.name}",
                             description="\n".join(lines),
                             color=discord.Color.gold())
        )

async def setup(bot):
    await bot.add_cog(Levels(bot))