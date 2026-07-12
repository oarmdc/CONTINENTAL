import discord
from discord.ext import commands
import yt_dlp
from utils import update_presence, make_embed, send_error_embed, send_success_embed

class mainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_guild_remove")
    @commands.Cog.listener("on_guild_join")
    async def on_guild_change(self, guild):
        print(f"Guild change: {guild.name}, now in {len(self.bot.guilds)} servers")
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
    
    @commands.command()
    async def pfp(self, ctx, thatuser: discord.Member = None):
        target = thatuser or ctx.author
        embed = make_embed(ctx, f"{target.name}'s avatar", image=target.display_avatar.url, color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    async def play(self, ctx, *, query=None):
        if ctx.author.voice is None:
            await send_error_embed(ctx, "You are not connected to a voice channel.")
            return
        if ctx.voice_client is not None and ctx.voice_client.channel != ctx.author.voice.channel:
            await send_error_embed(ctx, "I'm already playing in another channel...")
            return
        if query is None:
            await send_error_embed(ctx, "Dont forget to add the song name/url...")
            return
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect(self_deaf=True)
        
        ydl_opts = {"format": "bestaudio", "noplaylist": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
            stream_url = info["url"]
        source = discord.FFmpegPCMAudio(stream_url)
        ctx.voice_client.play(source)
        
        await ctx.send(embed=make_embed(ctx, f"Now playing {info['title']}", image=info['thumbnail'], color=discord.Color.light_grey()))
    
    @commands.command()
    async def stop(self, ctx):
        if ctx.author.voice is None:
            await send_error_embed(ctx, "You are not connected to a voice channel.")
            return
        if ctx.voice_client is None:
            await send_error_embed(ctx, "I'm not connected to a voice channel.")
            return
        if not ctx.voice_client.is_playing():
            await send_error_embed(ctx, "Nothing is playing right now.")
            return
        ctx.voice_client.stop()
        await send_success_embed(ctx, "Music is now stopped.")

    @commands.command()
    async def disconnect(self, ctx):
        ...

async def setup(bot):
    await bot.add_cog(mainCommands(bot))