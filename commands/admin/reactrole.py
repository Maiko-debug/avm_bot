import discord
from discord.ext import commands
import json
import os
import re

REACT_PATH = "data/reactroles.json"
os.makedirs("data", exist_ok=True)

def load_react_roles():
    if not os.path.exists(REACT_PATH):
        with open(REACT_PATH, "w") as f:
            json.dump({}, f, indent=4)
    with open(REACT_PATH, "r") as f:
        return json.load(f)

def save_react_roles(data):
    with open(REACT_PATH, "w") as f:
        json.dump(data, f, indent=4)

class ReactRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.react_data = load_react_roles()

    @commands.command(name="reactrole")
    @commands.has_permissions(manage_roles=True)
    async def reactrole(self, ctx, message_link: str, role: discord.Role, emoji: str):
        try:
            match = re.search(r"/channels/(\d+)/(\d+)/(\d+)", message_link)
            if not match:
                raise ValueError("Invalid message link format.")

            guild_id, channel_id, message_id = map(int, match.groups())
            if ctx.guild.id != guild_id:
                raise ValueError("Message must be from this server.")

            channel = ctx.guild.get_channel(channel_id)
            message = await channel.fetch_message(message_id)

            await message.add_reaction(emoji)

            emoji_str = str(discord.PartialEmoji.from_str(emoji))

            # Save react role
            key = f"{guild_id}-{message_id}"
            self.react_data[key] = {
                "role_id": role.id,
                "emoji": emoji_str
            }
            save_react_roles(self.react_data)

            confirm = await ctx.send(f"✅ Reaction role added to [this message]({message_link})", delete_after=6)

        except Exception as e:
            confirm = await ctx.send(f"❌ Failed to set react role: {e}", delete_after=8)

        await ctx.message.delete(delay=2)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member is None or payload.guild_id is None:
            return

        key = f"{payload.guild_id}-{payload.message_id}"
        data = self.react_data.get(key)

        if data and str(payload.emoji) == data["emoji"]:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(data["role_id"])
            member = payload.member

            if role and role not in member.roles:
                try:
                    await member.add_roles(role, reason="Reaction role")
                except Exception as e:
                    print(f"[ReactRole Error] Add: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id is None or payload.user_id == self.bot.user.id:
            return

        key = f"{payload.guild_id}-{payload.message_id}"
        data = self.react_data.get(key)

        if data and str(payload.emoji) == data["emoji"]:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(data["role_id"])
            member = guild.get_member(payload.user_id)

            if role and member and role in member.roles:
                try:
                    await member.remove_roles(role, reason="Reaction role removed")
                except Exception as e:
                    print(f"[ReactRole Error] Remove: {e}")

async def setup(bot):
    await bot.add_cog(ReactRole(bot))
