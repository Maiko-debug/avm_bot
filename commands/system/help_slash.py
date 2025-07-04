import discord
from discord.ext import commands
from discord import app_commands

class AVMHelp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="avmhelp", description="Show available AVM commands")
    async def help_command(self, interaction: discord.Interaction):
        user = interaction.user
        perms = user.guild_permissions

        embed = discord.Embed(
            title="🧠 AVM Bot Help",
            description="Here are the commands available to you:",
            color=discord.Color.teal()
        )

        if perms.kick_members or perms.ban_members or perms.moderate_members:
            embed.add_field(
                name="🛠 Moderation",
                value="`!mute`, `!unmute`, `!ban`, `!unban`, `!purge`",
                inline=False
            )

        if perms.manage_guild:
            embed.add_field(
                name="📌 Config & Setup",
                value="`!set <type>` — set welcome/modlog\n`!unset <type>` — remove config\n`/setmodlog`, `/avmconfig`, `/status`",
                inline=False
            )
            embed.add_field(
                name="🪄 Welcome System",
                value="`!setwelcome`, `!resetwelcome`, `!previewwelcome`",
                inline=False
            )
            embed.add_field(
                name="🎨 Custom Embeds",
                value="`!embed Title | Description | #channel | #hexcolor`",
                inline=False
            )
            embed.add_field(
                name="🏷️ Role Tools",
                value="`!giverole`, `!removerole`, `!reactrole <link> <@role> <emoji>`",
                inline=False
            )
            embed.add_field(
                name="🧃 Triggers (Auto-Mod)",
                value="`!addtrigger`, `!removetrigger`, `!listtriggers`",
                inline=False
            )

        if not (perms.manage_guild or perms.kick_members):
            embed.add_field(
                name="🎉 Public Commands",
                value="None yet — but you're safe from the bot... for now.",
                inline=False
            )

        embed.set_footer(text="AVM — crafted for real server control and good vibes.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AVMHelp(bot))
