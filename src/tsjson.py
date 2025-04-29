import json
import discord

def get_guild_json() -> dict:
    """
    Reads the guilds from the json file and returns them as a dict.
    
    Returns:
        dict: A dictionary with the guild id as the key and a dictionary containing
              the guild name and a boolean indicating if the bot is enabled in the guild.
    """
    with open("json/guilds.json", "r") as f:
        data = json.load(f)
    return data

def write_guild_json(data: dict) -> None:
    """
    Writes the given data to the guilds json file.
    
    Args:
        data (dict): A dictionary with the guild id as the key and a dictionary containing
                    the guild name and a boolean indicating if the bot is enabled in the guild.
    """
    with open("json/guilds.json", "w") as f:
        json.dump(data, f, indent=4)

def check_guild_installed(guild: discord.Guild) -> None:
    """
    Checks if a guild is in the disabled guilds json file. If it isn't, it adds it
    with the bot enabled.

    Args:
        guild (discord.Guild): The guild to check.
    """
    data = get_guild_json()
    if str(guild.id) not in data:
        new_guild = {
            "name": guild.name,
            "enabled": True,
            "stick_timeout": 120
        }
        data[guild.id] = new_guild
        write_guild_json(data)
    
def enable_guild(guild: discord.Guild) -> None:
    """
    Enables the bot in the given guild. If the guild is not in the disabled guilds
    json file, it adds it with the bot enabled.

    Args:
        guild (discord.Guild): The guild to enable the bot in.
    """
    check_guild_installed(guild)
    data = get_guild_json()
    data[str(guild.id)]["enabled"] = True
    write_guild_json(data)

def disable_guild(guild: discord.Guild) -> None:
    """
    Disables the bot in the given guild. If the guild is not in the disabled guilds
    json file, it adds it with the bot disabled.

    Args:
        guild (discord.Guild): The guild to disable the bot in.
    """
    check_guild_installed(guild)
    data = get_guild_json()
    data[str(guild.id)]["enabled"] = False
    write_guild_json(data)

def is_guild_enabled(guild: discord.Guild) -> bool:
    """
    Checks if the bot is enabled in the given guild.

    Args:
        guild (discord.Guild): The guild to check.

    Returns:
        bool: True if the bot is enabled in the guild, False otherwise.
    """
    check_guild_installed(guild)
    data = get_guild_json()
    return data[str(guild.id)]["enabled"]

def get_stick_timeout(guild: discord.Guild) -> int:
    """
    Gets the talking stick timeout for the given guild.

    Args:
        guild (discord.Guild): The guild to get the timeout for.

    Returns:
        int: The timeout in seconds.
    """
    check_guild_installed(guild)
    data = get_guild_json()
    return data[str(guild.id)]["stick_timeout"]

def set_stick_timeout(guild: discord.Guild, timeout: int) -> None:
    """
    Sets the talking stick timeout for the given guild.

    Args:
        guild (discord.Guild): The guild to set the timeout for.
        timeout (int): The timeout in seconds.
    """
    check_guild_installed(guild)
    data = get_guild_json()
    data[str(guild.id)]["stick_timeout"] = timeout
    write_guild_json(data)