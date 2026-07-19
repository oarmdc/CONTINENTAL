import discord
from discord import app_commands
from utils import make_embed, send_error_embed, send_success_embed
import calendar
import datetime
from discord.ext import commands, tasks

MIDNIGHT = datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc)

class mainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def cog_load(self):
        await self.bot.db.execute("""
            CREATE TABLE IF NOT EXISTS birthdays (
                user_id INTEGER,
                day INTEGER,
                month INTEGER,
                PRIMARY KEY (user_id)
            )
        """)
        await self.bot.db.commit()
        self.birthday_check.start()
    
    @app_commands.command(description= "Get an avatar. Leave empty for your own, or mention someone to get theirs.")
    async def pfp(self, interaction: discord.Interaction, thatuser: discord.Member = None):
        target = thatuser or interaction.user
        embed = make_embed(interaction, f"{target.name}'s avatar", image=target.display_avatar.url, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Add your birthday - Get a notification every year")
    async def setbirthday(self, interaction: discord.Interaction, day: app_commands.Range[int, 1, 31], month: app_commands.Range[int, 1, 12]):
        if day > calendar.monthrange(2024, month)[1]:
            await send_error_embed(interaction, "That day doesn't exist in that month.")
            return
        await self.bot.db.execute("""
            INSERT INTO birthdays (user_id, day, month)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET day = ?, month = ?
        """, (interaction.user.id, day, month, day, month))
        await self.bot.db.commit()
        await send_success_embed(interaction, f"Birthday saved for {interaction.user.display_name}: **{day:02d}.{month:02d}.** 🎂")

    @app_commands.command(description="Remove your saved birthday")
    async def removebirthday(self, interaction: discord.Interaction):
        cursor = await self.bot.db.execute("DELETE FROM birthdays WHERE user_id = ?",
                                           (interaction.user.id,)
                                           )
        await self.bot.db.commit()
        if cursor.rowcount == 0:
            await send_error_embed(interaction, "You don't have a birthday saved.")
            return
        await send_success_embed(interaction, "Your birthday has been removed. 🗑️")

    @tasks.loop(time=MIDNIGHT)
    async def birthday_check(self):
        today = datetime.datetime.now(datetime.timezone.utc)
        async with self.bot.db.execute(
            "SELECT user_id FROM birthdays WHERE day = ? AND month = ?",
            (today.day, today.month)
        ) as cursor:
            rows = await cursor.fetchall()

        for (user_id,) in rows:
            try:
                user = await self.bot.fetch_user(user_id)
                await user.send(
                    embed=make_embed(None, "Happy Birthday! 🎂",
                                     description="CONTINENTAL wishes you a wonderful birthday! 🎉",
                                     color=discord.Color.gold())
                )
            except discord.Forbidden:
                pass

async def setup(bot):
    await bot.add_cog(mainCommands(bot))