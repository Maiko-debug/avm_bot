import discord
from discord.ext import commands
from utils.server_config import get_modlog_channel

REQUIRED_PERMISSIONS = {
    "kick_members": "Kick Members",
    "ban_members": "Ban Members",
    "moderate_members": "Timeout Members",
    "manage_messages": "Manage Messages"
}

class Diagnostics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            bot_member = guild.me
            perms = bot_member.guild_permissions
            missing = [name for perm, name in REQUIRED_PERMISSIONS.items() if not getattr(perms, perm)]

            report = f"[✅ Permissions OK in {guild.name}]" if not missing else f"[⚠️ Permissions Warning in {guild.name}]: Missing {', '.join(missing)}"
            print(report)

            # Try to DM owner
            try:
                owner = guild.owner
                dm = owner.dm_channel or await owner.create_dm()
                await dm.send(f"🛠️ AVM is online in **{guild.name}**.\n" + report)
            except Exception as e:
                print(f"Could not DM owner of {guild.name}: {e}")

                # Fallback: send to mod log if available
                modlog_id = get_modlog_channel(guild.id)
                if modlog_id:
                    channel = self.bot.get_channel(modlog_id)
                    if channel:
                        try:
                            await channel.send(f"⚠️ AVM could not DM the server owner.\n{report}")
                        except Exception as err:
                            print(f"Could not send to mod log in {guild.name}: {err}")

async def setup(bot):
    await bot.add_cog(Diagnostics(bot))
