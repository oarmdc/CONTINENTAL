import discord
from discord.ext import commands
from utils import make_embed, send_error_embed, send_success_embed

class adminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.id != ctx.guild.owner_id and member.id == ctx.guild.owner_id:
            await send_error_embed(ctx, "You can't ban the owner, man..")
            return
        if ctx.author.id != ctx.guild.owner_id and member.guild_permissions.administrator:
            await send_error_embed(ctx, "You can't ban another admin.")
            return
        await member.ban(reason=reason)
        await send_success_embed(ctx, f"{member.name} is now banned.")
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await send_error_embed(ctx, "You don't have permission to use this command.")
        elif isinstance(error, commands.MemberNotFound):
            await send_error_embed(ctx, "That user isn't in this server.")

async def setup(bot):
    await bot.add_cog(adminCommands(bot))