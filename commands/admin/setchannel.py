import discord
from discord.ext import commands
from utils.server_config import update_guild_config, get_guild_config, save_config, load_config

VALID_TYPES = {
    "welcome": "Welcome Channel",
    "modlog": "Mod Log Channel"
}

class SetChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set")
    @commands.has_permissions(manage_guild=True)
    async def set_channel(self, ctx, channel_type: str):
        channel_type = channel_type.lower()

        if channel_type not in VALID_TYPES:
            msg = await ctx.send(f"❌ Invalid type. Try one of: `{', '.join(VALID_TYPES.keys())}`")
            await ctx.message.delete(delay=2)
            await msg.delete(delay=5)
            return

        update_guild_config(ctx.guild.id, channel_type, ctx.channel.id)

        confirm = await ctx.send(f"✅ {VALID_TYPES[channel_type]} set to {ctx.channel.mention}")
        await ctx.message.delete(delay=2)
        await confirm.delete(delay=5)

    @commands.command(name="unset")
    @commands.has_permissions(manage_guild=True)
    async def unset_channel(self, ctx, channel_type: str):
        channel_type = channel_type.lower()

        if channel_type not in VALID_TYPES:
            msg = await ctx.send(f"❌ Invalid type. Try one of: `{', '.join(VALID_TYPES.keys())}`")
            await ctx.message.delete(delay=2)
            await msg.delete(delay=5)
            return

        config = load_config()
        gid = str(ctx.guild.id)

        if gid in config and channel_type in config[gid]:
            del config[gid][channel_type]
            save_config(config)
            confirm = await ctx.send(f"✅ {VALID_TYPES[channel_type]} has been unset.")
        else:
            confirm = await ctx.send(f"⚠️ {VALID_TYPES[channel_type]} was not set.")

        await ctx.message.delete(delay=2)
        await confirm.delete(delay=5)

async def setup(bot):
    await bot.add_cog(SetChannel(bot))
