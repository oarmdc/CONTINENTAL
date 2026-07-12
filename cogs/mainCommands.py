import discord
from discord.ext import commands
from utils import update_presence, make_embed, send_error_embed, send_success_embed

class mainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def pfp(self, ctx, thatuser: discord.Member = None):
        target = thatuser or ctx.author
        embed = make_embed(ctx, f"{target.name}'s avatar", image=target.display_avatar.url, color=discord.Color.blue())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(mainCommands(bot))