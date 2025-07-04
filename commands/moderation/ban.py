import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        try:
            await member.ban(reason=reason)
            confirm = await ctx.send(f"⛔ {member.mention} has been banned.")
        except discord.Forbidden:
            confirm = await ctx.send("❌ I don't have permission to ban that member.")
        except Exception as e:
            confirm = await ctx.send(f"⚠️ Ban failed: {e}")

        await ctx.message.delete(delay=2)
        await confirm.delete(delay=6)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason: str = "No reason provided"):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            confirm = await ctx.send(f"✅ {user.name} has been unbanned.")
        except discord.NotFound:
            confirm = await ctx.send("❌ User not found in the ban list.")
        except Exception as e:
            confirm = await ctx.send(f"⚠️ Unban failed: {e}")

        await ctx.message.delete(delay=2)
        await confirm.delete(delay=6)

async def setup(bot):
    await bot.add_cog(Ban(bot))
