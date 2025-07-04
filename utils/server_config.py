import json
import os

CONFIG_PATH = "data/config.json"

# Make sure data/ folder exists
os.makedirs("data", exist_ok=True)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump({}, f, indent=4)

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def update_guild_config(guild_id, key, value):
    config = load_config()
    gid = str(guild_id)
    if gid not in config:
        config[gid] = {}
    config[gid][key] = value
    save_config(config)

def get_guild_config(guild_id):
    config = load_config()
    return config.get(str(guild_id), {})

# Specific shortcuts for common fields
def get_modlog_channel(guild_id):
    return get_guild_config(guild_id).get("mod_log")

def get_welcome_channel(guild_id):
    return get_guild_config(guild_id).get("welcome")

def get_mute_duration(guild_id):
    return get_guild_config(guild_id).get("default_mute_duration", 10)

def is_auto_ban_enabled(guild_id):
    return get_guild_config(guild_id).get("auto_ban_enabled", True)

def get_trigger_response_type(guild_id):
    return get_guild_config(guild_id).get("trigger_response_type", "public")
