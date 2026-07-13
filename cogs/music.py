import discord
from discord.ext import commands
import wavelink
from utils import make_embed, send_error_embed, send_success_embed


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        player = payload.player
        if player and not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)
            await player.home.send(embed=make_embed(None, f"Playing now: {next_track.title}", image=next_track.artwork, color=discord.Color.light_grey()))

    @commands.command()
    async def play(self, ctx, *, query:str):
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
            player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            player.inactive_timeout = 300
        else:
            player = ctx.voice_client
        player.home = ctx.channel
        
        tracks = await wavelink.Playable.search(query)
        if not tracks:
            await send_error_embed(ctx, "No tracks found.")
            return
        track = tracks[0]
        if player.playing:
            player.queue.put(track)
            await ctx.send(embed=make_embed(ctx, f"Added to queue: {track.title}", thumbnail=track.artwork, color=discord.Color.light_grey()))
        else:
            await player.play(track)
            await ctx.send(embed=make_embed(ctx, f"Playing now: {track.title}", image=track.artwork, color=discord.Color.light_grey()))
    
    @commands.command()
    async def skip(self, ctx):
        if ctx.author.voice is None:
            await send_error_embed(ctx, "You are not connected to a voice channel.")
            return
        if ctx.voice_client is None:
            await send_error_embed(ctx, "I'm not connected to a voice channel.")
            return
        if not ctx.voice_client.playing and not ctx.voice_client.paused:
            await send_error_embed(ctx, "Nothing is playing right now.")
            return
        await ctx.voice_client.stop()
        await send_success_embed(ctx, "Skipped.")

    @commands.command()
    async def stop(self, ctx):
        if ctx.author.voice is None:
            await send_error_embed(ctx, "You are not connected to a voice channel.")
            return
        if ctx.voice_client is None:
            await send_error_embed(ctx, "I'm not connected to a voice channel.")
            return
        if not ctx.voice_client.playing and not ctx.voice_client.paused:
            await send_error_embed(ctx, "Nothing is playing right now.")
            return
        ctx.voice_client.queue.clear()
        await ctx.voice_client.stop()
        await send_success_embed(ctx, "Music is now stopped.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice is None:
            await send_error_embed(ctx, "You are not connected to a voice channel.")
            return
        if ctx.voice_client is None:
            await send_error_embed(ctx, "I'm not connected to a voice channel.")
            return
        ctx.voice_client.queue.clear()
        await ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await send_success_embed(ctx, "I am now disconnected from the voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))