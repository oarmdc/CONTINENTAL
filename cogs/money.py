import discord
from discord.ext import commands
from discord import app_commands
from utils import send_error_embed, send_success_embed, make_embed
import time
import random

class Money(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

    async def cog_load(self):
        await self.bot.db.execute("""
            CREATE TABLE IF NOT EXISTS money (
                user_id INTEGER,
                balance INTEGER DEFAULT 0,
                public INTEGER DEFAULT 1,
                last_daily INTEGER DEFAULT 0,
                PRIMARY KEY (user_id)
            )
        """)
        await self.bot.db.commit()

    @app_commands.command(description="Top up money")
    @app_commands.describe(amount="Amount of money to top up", member="Receiver [Leave empty for selftopup]")
    @app_commands.checks.has_permissions(administrator=True)
    async def topup(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1], member: discord.Member = None):
        member = member or interaction.user
        await self.bot.db.execute("""
            INSERT INTO money (user_id, balance)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET balance = balance + ?
        """, (member.id, amount, amount))
        await self.bot.db.commit()
        await interaction.response.send_message(embed=make_embed(interaction,
                                                                f"Money added to {member.name}!",
                                                                thumbnail="https://i.pinimg.com/736x/61/b4/e0/61b4e0456d99894da978a153a4030320.jpg",
                                                                description=f"{interaction.user.name} topped {amount}USD to {member.name} up!"))
    @topup.error
    async def topup_error(self, interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await send_error_embed(interaction, "You don't have permission to use this command.")

    @app_commands.command(description="Check your/your friend's balance")
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        async with self.bot.db.execute("SELECT balance, public FROM money WHERE user_id = ?",
                               (member.id,)
                               ) as cursor:
            row = await cursor.fetchone()
        if row is None:
            await send_error_embed(interaction, f"{member.display_name} has no balance yet.")
            return
        balance, public = row
        if public == 0 and member.id != interaction.user.id:
            await send_error_embed(interaction, f"{member.name}'s balance is private...")
            return
        ephemeral = (public == 0)
        await interaction.response.send_message(embed=make_embed(interaction,
                                                                            f"{member.name}'s balance:",
                                                                            thumbnail="https://i.pinimg.com/736x/61/b4/e0/61b4e0456d99894da978a153a4030320.jpg",
                                                                            description=f"{balance}USD"),
                                                                            ephemeral=ephemeral
                                                                            )
        
    @app_commands.command(description="Set your balance privacy")
    @app_commands.describe(choice="1 for public, 0 for private")
    async def setprivacy(self, interaction: discord.Interaction, choice: app_commands.Range[int, 0, 1]):
        await self.bot.db.execute("""
            INSERT INTO money (user_id, public)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET PUBLIC = ?
        """, (interaction.user.id, choice, choice))
        await self.bot.db.commit()
        state = "public" if choice == 1 else "private"
        await send_success_embed(interaction, f"Your balance is now **{state}**.")

    @app_commands.command(description="Send money to someone else")
    @app_commands.describe(member="Receiver", amount="Amount of money to send in USD")
    async def sendmoney(self, interaction: discord.Interaction, member: discord.Member, amount: app_commands.Range[int, 1]):
        if member.id == interaction.user.id:
            await send_error_embed(interaction, "You can't send money to yourself.")
            return
        if member.bot:
            await send_error_embed(interaction, "You can't send money to a bot.")
            return
        async with self.bot.db.execute("SELECT balance FROM money WHERE user_id = ?",
                                       (interaction.user.id,)
                                       ) as cursor:
                    row = await cursor.fetchone()
        if row is None:
            await send_error_embed(interaction, f"{interaction.user.display_name} has no balance yet.")
            return
        senderbalance = row[0]
        if (senderbalance < amount):
             await send_error_embed(interaction, f"You don't have enough money to do that... Your balance is: {senderbalance}")
             return
        await self.bot.db.execute("""
            INSERT INTO money (user_id, balance)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET balance = balance + ?
        """, (member.id, amount, amount))
        await self.bot.db.execute("""
            INSERT INTO money (user_id, balance)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET balance = balance - ?
        """, (interaction.user.id, amount, amount))
        await self.bot.db.commit()
        await send_success_embed(interaction, f"Done! {amount}USD have been transferred to {member.display_name}")

    @app_commands.command(description="Claim your daily money")
    async def daily(self, interaction: discord.Interaction):
        now = int(time.time())
        async with self.bot.db.execute("SELECT last_daily FROM money WHERE user_id = ?",
                                   (interaction.user.id,)
                                   ) as cursor:
            row = await cursor.fetchone()
        last_daily = row[0] if row else 0
        elapsed = now - last_daily
        if elapsed < 86400:
            remaining = 86400 - elapsed
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            await send_error_embed(interaction, f"You already claimed today. Try again in {hours}h {minutes}m.")
            return
        reward = random.randint(50, 150)
        await self.bot.db.execute("""
            INSERT INTO money (user_id, balance, last_daily)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET balance = balance + ?, last_daily = ?
        """, (interaction.user.id, reward, now, reward, now))
        await self.bot.db.commit()
        await send_success_embed(interaction, f"You claimed your daily reward: **{reward}**USD.")
        

         

async def setup(bot):
    await bot.add_cog(Money(bot))