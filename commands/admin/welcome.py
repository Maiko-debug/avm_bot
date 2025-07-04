import discord
from discord.ext import commands
from utils.server_config import get_welcome_channel, get_guild_config, update_guild_config

DEFAULT_WELCOME = """🌌✨ WELCOME TO AVM, {user}! ✨🌌
╔═════════★🌟★═════════╗
🎮 Gamers. Dreamers. Night Owls. Legends.
🎧 Chill with music.
🕹 Squad up for games.
💬 Late-night talks or pure chaos — your choice.

👑 You didn’t just join a server…
You entered a vibe sanctuary where friendships are forged,
memes are sacred, and good energy is the law.

🎉 We’re a mix of cozy chaos, genuine people, and epic moments.
And now… you’re part of it.
╚═════════★🌟★═════════╝

🌠 Drop a hi, claim your space, and let the good times roll. Welcome home."""

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel_id = get_welcome_channel(member.guild.id)
        if not channel_id:
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        config = get_guild_config(member.guild.id)
        welcome_msg = config.get("welcome_message", DEFAULT_WELCOME)
        welcome_text = welcome_msg.format(user=member.mention)

        embed = discord.Embed(
            title="🎉 A New Legend Has Arrived!",
            description=welcome_text,
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Welcome to AVM")

        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"[WELCOME ERROR] {e}")

    @commands.command(name="setwelcome")
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, *, message: str):
        update_guild_config(ctx.guild.id, "welcome_message", message)
        confirm = await ctx.send("✅ Welcome message updated!", delete_after=5)
        await ctx.message.delete(delay=2)
        await confirm.delete(delay=5)

    @commands.command(name="resetwelcome")
    @commands.has_permissions(manage_guild=True)
    async def resetwelcome(self, ctx):
        config = get_guild_config(ctx.guild.id)
        if "welcome_message" in config:
            del config["welcome_message"]
            update_guild_config(ctx.guild.id, "welcome_message", None)  # or save manually if needed
            confirm = await ctx.send("🔄 Welcome message reset to default!", delete_after=5)
        else:
            confirm = await ctx.send("⚠️ You're already using the default welcome message.", delete_after=5)

        await ctx.message.delete(delay=2)
        await confirm.delete(delay=5)

    @commands.command(name="previewwelcome")
    @commands.has_permissions(manage_guild=True)
    async def previewwelcome(self, ctx):
        config = get_guild_config(ctx.guild.id)
        welcome_msg = config.get("welcome_message", DEFAULT_WELCOME)
        welcome_text = welcome_msg.format(user=ctx.author.mention)

        embed = discord.Embed(
            title="👀 Preview: AVM Welcome",
            description=welcome_text,
            color=discord.Color.purple()
        )
        embed.set_footer(text="This is a preview. Only you can see this.")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete(delay=2)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
