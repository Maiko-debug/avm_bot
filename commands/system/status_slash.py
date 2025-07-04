import discord
from discord.ext import commands
from discord import app_commands
from utils.server_config import (
    get_modlog_channel,
    get_welcome_channel
)

REQUIRED_PERMISSIONS = {
    "kick_members": "Kick Members",
    "ban_members": "Ban Members",
    "moderate_members": "Timeout Members",
    "manage_messages": "Manage Messages"
}

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="status", description="Check AVM's bot health and permissions")
    async def status(self, interaction: discord.Interaction):
        bot_member = interaction.guild.me
        perms = bot_member.guild_permissions
        missing = [label for perm, label in REQUIRED_PERMISSIONS.items() if not getattr(perms, perm)]

        role_pos = bot_member.top_role.position
        top_role_pos = interaction.guild.roles[-1].position

        modlog_id = get_modlog_channel(interaction.guild_id)
        welcome_id = get_welcome_channel(interaction.guild_id)

        embed = discord.Embed(
            title="📊 AVM Bot Status",
            color=discord.Color.green() if not missing else discord.Color.orange()
        )
        embed.add_field(name="🤖 Bot", value=f"{bot_member.mention} is online", inline=False)
        embed.add_field(name="🎖 Role Position", value=f"{role_pos} / {top_role_pos}", inline=True)

        if missing:
            embed.add_field(name="❌ Missing Permissions", value="• " + "\n• ".join(missing), inline=False)
        else:
            embed.add_field(name="✅ Permissions", value="All required permissions are active", inline=False)

        embed.add_field(
            name="📌 Channels",
            value=(
                f"Mod Log: {f'<#{modlog_id}>' if modlog_id else 'Not set'}\n"
                f"Welcome: {f'<#{welcome_id}>' if welcome_id else 'Not set'}"
            ),
            inline=False
        )
        embed.set_footer(text="Run /status anytime to check AVM's health.")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Status(bot))
