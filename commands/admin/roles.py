import discord
from discord.ext import commands

class RoleAssign(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="giverole")
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, member: discord.Member, *, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if not role:
            msg = await ctx.send(f"❌ Role `{role_name}` not found.", delete_after=5)
        elif role >= ctx.guild.me.top_role:
            msg = await ctx.send("⚠️ I can't assign roles higher than mine.", delete_after=5)
        else:
            await member.add_roles(role)
            msg = await ctx.send(f"✅ {member.mention} was given `{role.name}`.")

        await ctx.message.delete(delay=2)
        await msg.delete(delay=5)

    @commands.command(name="removerole")
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, *, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if not role or role not in member.roles:
            msg = await ctx.send(f"⚠️ {member.mention} does not have `{role_name}`.", delete_after=5)
        else:
            await member.remove_roles(role)
            msg = await ctx.send(f"🗑️ Removed `{role.name}` from {member.mention}.")

        await ctx.message.delete(delay=2)
        await msg.delete(delay=5)

async def setup(bot):
    await bot.add_cog(RoleAssign(bot))
