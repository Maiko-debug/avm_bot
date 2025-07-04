import discord
from discord.ext import commands

class EmbedMaker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.command(name="embed")
@commands.has_permissions(manage_guild=True)
async def embed(self, ctx, *, args: str):
    try:
        parts = [p.strip() for p in args.split("|")]
        if len(parts) < 2:
            raise ValueError("Missing title or description.")

        title = parts[0]
        desc = parts[1]
        target = ctx.channel
        color = discord.Color.blue()

        if len(parts) >= 3:
            if ctx.message.channel_mentions:
                target = ctx.message.channel_mentions[0]

        if len(parts) == 4:
            hex_code = parts[3].lstrip("#")
            try:
                color = discord.Color(int(hex_code, 16))
            except ValueError:
                raise ValueError("Invalid hex color code (must be like `#ffcc00`).")

        embed = discord.Embed(title=title, description=desc, color=color)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await target.send(embed=embed)
        msg = await ctx.send(f"✅ Embed sent to {target.mention}.", delete_after=5)

    except Exception as e:
        msg = await ctx.send(f"❌ Failed to send embed: {e}", delete_after=6)

    await ctx.message.delete(delay=2)

async def setup(bot):
    await bot.add_cog(EmbedMaker(bot))
