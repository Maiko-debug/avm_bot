import discord
from discord.ext import commands
from datetime import timedelta
from utils.server_config import get_mute_duration

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int = None, *, reason: str = "No reason provided"):
        try:
            duration = timedelta(minutes=minutes if minutes else get_mute_duration(ctx.guild.id))
            await member.timeout(duration, reason=reason)
            confirm = await ctx.send(f"🔇 {member.mention} has been muted for {duration.total_seconds() // 60:.0f} minutes.")
        except discord.Forbidden:
            confirm = await ctx.send("❌ I don't have permission to mute that member.")
        except Exception as e:
            confirm = await ctx.send(f"⚠️ Mute failed: {e}")

        await ctx.message.delete(delay=2)
        await confirm.delete(delay=6)

    @commands.command(name="unmute")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        try:
            await member.timeout(None, reason=reason)
            confirm = await ctx.send(f"🔊 {member.mention} has been unmuted.")
        except discord.Forbidden:
            confirm = await ctx.send("❌ I don't have permission to unmute that member.")
        except Exception as e:
            confirm = await ctx.send(f"⚠️ Unmute failed: {e}")

        await ctx.message.delete(delay=2)
        await confirm.delete(delay=6)

async def setup(bot):
    await bot.add_cog(Mute(bot))
