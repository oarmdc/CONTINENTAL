import discord
from discord.ext import commands
from discord import app_commands
import wavelink
from utils import make_embed, send_error_embed, send_success_embed


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        if payload.reason == "loadFailed":
            return
        player = payload.player
        if player and not player.queue.is_empty:
            next_track = player.queue.get()
            player.retried = False
            await player.play(next_track)
            await player.home.send(embed=make_embed(None, f"Playing now: {next_track.title}", image=next_track.artwork, color=discord.Color.light_grey()))
        elif player and payload.reason == "finished":
            await player.home.send(embed=make_embed(None, "Queue finished.", color=discord.Color.light_grey()))

    @commands.Cog.listener()
    async def on_wavelink_track_exception(self, payload: wavelink.TrackExceptionEventPayload):
        player = payload.player
        if player is None:
            return
        if not getattr(player, "retried", False):
            player.retried = True
            await player.play(payload.track)
        else:
            player.retried = False
    
    @app_commands.command()
    async def play(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        if interaction.user.voice is None:
            await send_error_embed(interaction, "You are not connected to a voice channel.")
            return
        if interaction.guild.voice_client is not None and interaction.guild.voice_client.channel != interaction.user.voice.channel:
            await send_error_embed(interaction, "I'm already playing in another channel...")
            return
        if interaction.guild.voice_client is None:
            player = await interaction.user.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            player.inactive_timeout = 300
        else:
            player = interaction.guild.voice_client
        player.home = interaction.channel
        
        tracks = await wavelink.Playable.search(query)
        if not tracks:
            await send_error_embed(interaction, "No tracks found.")
            return
        track = tracks[0]
        if player.playing or player.current:
            player.queue.put(track)
            await interaction.followup.send(embed=make_embed(interaction, f"Added to queue: {track.title}", thumbnail=track.artwork, color=discord.Color.light_grey()))
        else:
            player.retried = False
            await player.play(track)
            await interaction.followup.send(embed=make_embed(interaction, f"Playing now: {track.title}", image=track.artwork, color=discord.Color.light_grey()))
    
    @app_commands.command()
    async def skip(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await send_error_embed(interaction, "You are not connected to a voice channel.")
            return
        if interaction.guild.voice_client is None:
            await send_error_embed(interaction, "I'm not connected to a voice channel.")
            return
        if not interaction.guild.voice_client.playing and not interaction.guild.voice_client.paused:
            await send_error_embed(interaction, "Nothing is playing right now.")
            return
        await interaction.guild.voice_client.stop()
        await send_success_embed(interaction, "Skipped.")

    @app_commands.command()
    async def stop(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await send_error_embed(interaction, "You are not connected to a voice channel.")
            return
        if interaction.guild.voice_client is None:
            await send_error_embed(interaction, "I'm not connected to a voice channel.")
            return
        if not interaction.guild.voice_client.playing and not interaction.guild.voice_client.paused:
            await send_error_embed(interaction, "Nothing is playing right now.")
            return
        interaction.guild.voice_client.queue.clear()
        await interaction.guild.voice_client.stop()
        await send_success_embed(interaction, "Music is now stopped.")

    @app_commands.command()
    async def leave(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await send_error_embed(interaction, "You are not connected to a voice channel.")
            return
        if interaction.guild.voice_client is None:
            await send_error_embed(interaction, "I'm not connected to a voice channel.")
            return
        interaction.guild.voice_client.queue.clear()
        await interaction.guild.voice_client.stop()
        await interaction.guild.voice_client.disconnect()
        await send_success_embed(interaction, "I am now disconnected from the voice channel.")

    @app_commands.command()
    async def queue(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None or interaction.guild.voice_client.queue.is_empty:
            await send_error_embed(interaction, "The queue is empty.")
            return
        songs = "\n".join(f"{i+1}. {track.title}" for i, track in enumerate(interaction.guild.voice_client.queue))
        await interaction.response.send_message(embed=make_embed(interaction, "Queue", description=songs, color=discord.Color.light_grey()))

async def setup(bot):
    await bot.add_cog(music(bot))