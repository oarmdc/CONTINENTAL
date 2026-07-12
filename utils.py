import discord

def parse(text, start, end):
    start_index = text.find(start) + len(start)
    end_index = text.find(end, start_index)
    if start_index == -1 or end_index == -1:
        return None
    return text[start_index:end_index]

async def update_presence(thatbot):
    await thatbot.change_presence(
        activity=discord.Game(name=f"with {len(thatbot.guilds)} servers!")
        )
    
async def make_embed(ctx, title, *, image=None, thumbnail=None, description=None, color=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    embed.set_author(
        name=f"Command requested by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )
    embed.set_footer(text="coded by oarm")
    return embed

async def send_error_embed(ctx, message):
    await ctx.send(embed=make_embed(ctx, "Error", description=message, color=discord.Color.red()))

async def send_success_embed(ctx, message):
    await ctx.send(embed=make_embed(ctx, "Success", description=message, color=discord.Color.green()))