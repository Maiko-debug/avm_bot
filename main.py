import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# GUILD_ID is not strictly needed if you're only doing global syncs for now,
# but keeping it here doesn't hurt.
GUILD_ID = '1381345238395785277' # Your server ID (as a string)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"[READY] {bot.user} is online!")
    await load_cogs() # Load all your command cogs
    try:
        # Perform a GLOBAL sync. This is what's consistently working for you.
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} global commands.")
        for cmd in synced:
            print(f" - /{cmd.name}") # Print the names of synced commands
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def load_cogs():
    cogs_dir = './commands'
    print("[EXTENSION] Loading all cogs...") # Added clearer print
    for root, dirs, files in os.walk(cogs_dir):
        relative_path = os.path.relpath(root, cogs_dir)

        for filename in files:
            if filename.endswith('.py'):
                if relative_path == ".":
                    extension_path = f'commands.{filename[:-3]}'
                else:
                    folder_path = relative_path.replace(os.sep, '.')
                    extension_path = f'commands.{folder_path}.{filename[:-3]}'
                try:
                    await bot.load_extension(extension_path)
                    print(f" - Loaded: {extension_path}") # Added clearer print
                except Exception as e:
                    print(f" - [ERROR] Failed to load {extension_path}: {e}") # Improved error print

# Add a check for the TOKEN for better startup robustness
if __name__ == "__main__":
    if TOKEN is None:
        print("[ERROR] DISCORD_TOKEN environment variable not set. Exiting.")
        exit(1)
    bot.run(TOKEN)
