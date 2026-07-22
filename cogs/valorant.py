import discord
from discord import app_commands
from discord.ext import commands
from utils import make_embed, send_error_embed
import os
import asyncio
import requests
from urllib.parse import quote

HENRIK_BASE = "https://api.henrikdev.xyz"
TIER_ASSET_VERSION = "03621f52-342b-cf4e-4f86-9350a49c6d04"

RANK_COLORS = {
    "iron": 0x4C4C52,
    "bronze": 0x8A5A34,
    "silver": 0xA9AFB8,
    "gold": 0xE8C547,
    "platinum": 0x36C4B3,
    "diamond": 0xB265E0,
    "ascendant": 0x2FCB70,
    "immortal": 0xB2264F,
    "radiant": 0xF3F4B0,
}
DEFAULT_COLOR = 0x2F3136

def rank_color(tier_name: str) -> int:
    key = tier_name.split(" ")[0].lower() if tier_name else ""
    return RANK_COLORS.get(key, DEFAULT_COLOR)

def rank_icon(tier_id: int):
    if not tier_id:
        return None
    return f"https://media.valorant-api.com/competitivetiers/{TIER_ASSET_VERSION}/{tier_id}/smallicon.png"

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _get(self, interaction: discord.Interaction, url: str):
        try:
            resp = await asyncio.to_thread(
                requests.get, url, headers={"Authorization": os.getenv("HENRIK_API_KEY")}, timeout=10
            )
        except requests.RequestException:
            await send_error_embed(interaction, "Couldn't reach the Valorant API. Please try again in a moment.")
            return None

        if resp.status_code == 404:
            await send_error_embed(interaction, "Couldn't find that player. Double-check the name and tag.")
            return None
        if resp.status_code == 429:
            await send_error_embed(interaction, "The Valorant API is rate limiting requests. Try again shortly.")
            return None
        if resp.status_code != 200:
            message = "Unknown error."
            try:
                message = resp.json().get("errors", [{}])[0].get("message", message)
            except (ValueError, IndexError, AttributeError):
                pass
            await send_error_embed(interaction, f"Valorant API error: {message}")
            return None

        return resp.json().get("data")

    @app_commands.command(description="Get a player's Valorant stats")
    @app_commands.describe(username="Riot ID name", tag="Riot ID tag (without the #)")
    async def valorant(self, interaction: discord.Interaction, username: str, tag: app_commands.Range[str, 3, 5]):
        await interaction.response.defer()

        try:
            name_part = quote(username)
            tag_part = quote(tag)

            account = await self._get(interaction, f"{HENRIK_BASE}/valorant/v1/account/{name_part}/{tag_part}")
            if account is None:
                return

            region = account.get("region")
            if not region:
                await send_error_embed(interaction, "That account has no region on file. Try again later.")
                return

            mmr = await self._get(interaction, f"{HENRIK_BASE}/valorant/v3/mmr/{region}/pc/{name_part}/{tag_part}")
            if mmr is None:
                return

            current = mmr.get("current") or {}
            peak = mmr.get("peak") or {}

            tier_id = (current.get("tier") or {}).get("id") or 0
            tier_name = (current.get("tier") or {}).get("name") or "Unranked"
            rr = current.get("rr", 0)
            elo = current.get("elo", 0)
            last_change = current.get("last_change", 0)
            change_str = f"+{last_change}" if last_change > 0 else str(last_change)

            peak_tier_name = (peak.get("tier") or {}).get("name") or "Unranked"
            peak_season = ((peak.get("season") or {}).get("short") or "").upper()
            peak_str = f"{peak_tier_name} ({peak_season})" if peak_season else peak_tier_name

            card = account.get("card") or {}
            display_name = account.get("name") or username
            display_tag = account.get("tag") or tag

            embed = make_embed(
                interaction,
                f"{display_name}#{display_tag} — Valorant Stats",
                thumbnail=rank_icon(tier_id) or card.get("small"),
                image=card.get("wide"),
                color=rank_color(tier_name),
            )
            embed.url = f"https://tracker.gg/valorant/profile/riot/{quote(display_name)}%23{quote(display_tag)}/overview"

            embed.add_field(name="🏆 Rank", value=f"**{tier_name}**\n{rr} RR", inline=True)
            embed.add_field(name="📈 Peak Rank", value=peak_str, inline=True)
            embed.add_field(name="⚡ Elo", value=str(elo), inline=True)
            embed.add_field(name="🔄 Last Match", value=f"{change_str} RR", inline=True)
            embed.add_field(name="🎖️ Account Level", value=str(account.get("account_level", "—")), inline=True)
            embed.add_field(name="🌍 Region", value=region.upper(), inline=True)

            await interaction.followup.send(embed=embed)
        except Exception:
            await send_error_embed(interaction, "Something went wrong while fetching those stats. Please try again.")
            raise


async def setup(bot):
    await bot.add_cog(Valorant(bot))
