import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

REQUIRED_PERMISSIONS = {
    "kick_members": "Kick Members",
    "ban_members": "Ban Members",
    "moderate_members": "Timeout Members",
    "manage_messages": "Manage Messages"
}

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID", 0))

class Diagnostics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            print(f"[Diagnostics] Could not find log channel with ID {LOG_CHANNEL_ID}")
            return

        for guild in self.bot.guilds:
            bot_member = guild.me
            perms = bot_member.guild_permissions
            missing = [name for perm, name in REQUIRED_PERMISSIONS.items() if not getattr(perms, perm)]

            embed = discord.Embed(
                title=f"🔍 Permissions Check: {guild.name}",
                color=discord.Color.green() if not missing else discord.Color.red()
            )
            embed.set_footer(text=f"Guild ID: {guild.id}")

            if not missing:
                embed.description = "✅ All required permissions are present."
            else:
                embed.description = (
                    f"⚠️ **Missing Permissions:** {', '.join(missing)}\n"
                    f"🔻 *Role position may also prevent moderation actions.*"
                )

            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Diagnostics(bot))
