import discord
from discord.ext import commands
from datetime import timedelta
import os
import json

TRIGGER_PATH = "data/triggers.json"
os.makedirs("data", exist_ok=True)

def load_triggers():
    if not os.path.exists(TRIGGER_PATH):
        with open(TRIGGER_PATH, "w") as f:
            json.dump({}, f, indent=4)

    with open(TRIGGER_PATH, "r") as f:
        return json.load(f)

def save_triggers(triggers):
    with open(TRIGGER_PATH, "w") as f:
        json.dump(triggers, f, indent=4)

class Triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.triggers = load_triggers()  # {guild_id: {word: action}}

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def addtrigger(self, ctx, word: str, action: str = "mute"):
        gid = str(ctx.guild.id)
        if gid not in self.triggers:
            self.triggers[gid] = {}

        self.triggers[gid][word.lower()] = action.lower()
        save_triggers(self.triggers)
        await ctx.send(f"✅ Trigger `{word}` set to `{action}`.", delete_after=6)
        await ctx.message.delete(delay=2)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removetrigger(self, ctx, word: str):
        gid = str(ctx.guild.id)
        if gid in self.triggers and word.lower() in self.triggers[gid]:
            del self.triggers[gid][word.lower()]
            save_triggers(self.triggers)
            await ctx.send(f"✅ Trigger `{word}` removed.", delete_after=6)
        else:
            await ctx.send("⚠️ That trigger doesn't exist.", delete_after=6)

        await ctx.message.delete(delay=2)

    @commands.command()
    async def listtriggers(self, ctx):
        gid = str(ctx.guild.id)
        if gid not in self.triggers or not self.triggers[gid]:
            msg = await ctx.send("📭 No active triggers.")
        else:
            msg = "**🪄 Current Triggers:**\n"
            for word, act in self.triggers[gid].items():
                msg += f"• `{word}` → `{act}`\n"
            await ctx.send(msg)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        gid = str(message.guild.id)
        content = message.content.lower()

        if gid not in self.triggers:
            return

        for word, action in self.triggers[gid].items():
            if word in content:
                try:
                    if action == "mute":
                        duration = timedelta(minutes=10)
                        await message.author.timeout(duration, reason=f"Triggered word: {word}")
                        await message.channel.send(
                            f"🚫 {message.author.mention} has been muted (triggered: `{word}`)", delete_after=6
                        )

                    elif action == "ban":
                        await message.author.ban(reason=f"Triggered word: {word}")
                        await message.channel.send(
                            f"⛔ {message.author.mention} has been banned (triggered: `{word}`)", delete_after=6
                        )

                except discord.Forbidden:
                    await message.channel.send("⚠️ I lack permissions to moderate this member.", delete_after=6)
                except Exception as e:
                    print(f"[TRIGGER ERROR] {e}")

                break  # only act on first trigger

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Triggers(bot))
