import discord

async def update_presence(thatbot):
    await thatbot.change_presence(
        activity=discord.Game(name=f"with {len(thatbot.guilds)} servers!")
        )
    
def make_embed(interaction, title, *, image=None, thumbnail=None, description=None, color=None, timestamp=None, author=None):
    embed = discord.Embed(title=title, description=description, color=color, timestamp=timestamp)
    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if author:
        embed.set_author(name=author[0], icon_url=author[1])
    elif interaction is not None:
        embed.set_author(
            name=f"Command requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )
    embed.set_footer(text="coded by oarm & camarovx")
    return embed

async def send_error_embed(interaction, message):
    await interaction.response.send_message(embed=make_embed(interaction, "Error", description=message, color=discord.Color.red()), ephemeral=True)

async def send_success_embed(interaction, message):
    await interaction.response.send_message(embed=make_embed(interaction, "Success", description=message, color=discord.Color.green()), ephemeral=True)