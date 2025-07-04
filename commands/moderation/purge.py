import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        try:
            deleted = await ctx.channel.purge(limit=amount + 1, check=lambda m: not m.pinned)
            confirm = await ctx.send(f"🧹 Deleted {len(deleted)-1} messages.", delete_after=5)
        except Exception as e:
            confirm = await ctx.send(f"❌ Failed to purge: {e}", delete_after=5)

        await ctx.message.delete(delay=1)

async def setup(bot):
    await bot.add_cog(Purge(bot))
