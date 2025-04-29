import os
import discord
import src.ts as ts
import src.tsjson as tsjson
import src.stick_logger as logger
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.voice_states = True

log = logger.StickLogger()

# --- Add Feature ---
#TODO: [] Make Modules
#TODO: [] Add Super Stick (imune to mute)

# --- Bug Fixes ---

# --- Housekeeping ---
#TODO: [] Research nextcord
#TODO: [] Readme

# --- Completed ---
#TODO: [X] Add install scripts
#TODO: [X] Add error handling
#TODO: [X] Fix time complexity
#TODO: [X] Add logging
#TODO: [X] Set is ordered, it isn't working like a true queue
#TODO: [X] Add ability to clear queue
#TODO: [X] Stop the timer if end session is called
#TODO: [X] Fix 404 on disabled guild (refer to 404.txt)
#TODO: [X] Fix the enable and disable commands, make them enable or disable per guild
#TODO: [X] Move from a config file to config in json under guilds
#TODO: [X] Add help command
#TODO: [X] Clean up code, move to functions
#TODO: [X] Fix cancel timer if sitck is passed manually
#TODO: [X] Fix if someone leaves the voice channel, remove them from the queue
#TODO: [X] Fix if someone joins the voice channel, add them to the thread and mute them
#TODO: [X] Add Timeout
#TODO: [X] Add support for multiple talking stick sessions
#TODO: [X] Add support for multiple servers
#TODO: [X] Move away from global variables
#TODO: [X] Add private threads and add users who are in call with the stick owner to it
#TODO: [X] Add ping for who has the stick
#TODO: [X] Fix the 404 error that keeps occuring


class bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        """
        The constructor for the bot class.

        This class is a subclass of discord.Client and is used to create a bot that
        can connect to the Discord API and interact with the Discord client.

        The constructor takes one parameter, intents, which is an instance of
        discord.Intents. The intents parameter is used to specify which events the
        bot should receive from the Discord API.

        The constructor also creates a CommandTree instance, which is a special
        type of discord.TreeClient that is used to store and work with application
        commands.
        """
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.synced = False
        
    @tasks.loop(minutes=5)
    async def clear_sticks(self):
        """
        A task that is run every 60 seconds to clear the talking sticks.

        This task is used to clean up any sticks that are no longer being used.

        Parameters:
            self (bot): The bot instance.

        Returns:
            None
        """
        sticks_purged = stick_manager.purge_sticks()
        if sticks_purged > 0:
            log.log_info(f"Removed {sticks_purged} sticks.")

    async def setup_hook(self):
        """
        This function is called when the bot is setting up. It syncs the commands and
        creates the necessary tables in the database.
        """
        if not self.synced:
            # print('Clearing commands...')
            # self.tree.clear_commands(guild=None)
            # print('Syncing commands...')
            log.log_info('Syncing Commands...')
            await self.tree.sync()
            self.synced = True
        self.clear_sticks.start()
        log.log_info('Done!')
    
    

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        await self.change_presence(activity=discord.CustomActivity("Use /help"))
        log.log_info(f'{self.user} has connected to Discord!')

def check_admin(user: discord.User) -> bool:
    """
    Checks if the given user has an administrator role.

    This function iterates over the roles of the user and checks if any of them
    have administrator permissions.

    Parameters:
        user (discord.User): The Discord user to check.

    Returns:
        bool: True if the user has an administrator role, False otherwise.
    """
    for role in user.roles:
        if role.permissions.administrator:
            return True

bot = bot(intents=intents)
stick_manager = ts.StickManager()


# --- Utilities ---
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """
    This event is called when a user's voice state is changed. It's used by the bot
    to track when a user joins or leaves a voice channel.

    If the user has joined a voice channel, the bot will check if there is an
    existing talking stick session for the channel. If there is, the bot will
    add the user to the queue.

    If the user has left a voice channel, the bot will check if there is an
    existing talking stick session for the channel. If there is, the bot will
    remove the user from the queue.

    Parameters:
        member (discord.Member): The member whose voice state has changed.
        before (discord.VoiceState): The voice state for the member before the change.
        after (discord.VoiceState): The voice state for the member after the change.
    """
    if before.channel != after.channel and after.channel is not None:
        existing_stick = stick_manager.get_stick_by_channel(after.channel)
        if existing_stick is not None:
            try:
                await existing_stick.handle_user_joining(member)
                log.log_info(f"{member.name} joined {after.channel.name}")
            except Exception as e:
                log.log_error(e)
                member.send("An error occurred while joining the session.\nThe most likely cause is that you don't have permissions for the text channel in which the session was called from.\nPlease try again, or contact an admin.")
    if after.channel is None:
        existing_stick = stick_manager.get_stick_by_channel(before.channel)
        if existing_stick is not None:
            try:
                await existing_stick.handle_user_leaving(member)
                log.log_info(f"{member.name} removed from {before.channel.name}")
            except Exception as e:
                log.log_error(e)


# --- User Commands ---

@bot.tree.command(name="tsclaim", description="Claim the talking stick. If a talking stick session isn't started, it will start one.")
async def claim_stick(interaction: discord.Interaction):

    """
    Claims the talking stick.

    If a talking stick session isn't started, it will start one. If the user is not in a voice channel, it will send a message indicating that.

    Parameters:
        interaction (discord.Interaction): The interaction object containing information about the command invocation and the user who invoked the command.

    Returns:
        None
    """

    # Check if the user is in a voice channel
    if not interaction.user.voice:
        await interaction.response.send_message("You are not in a voice channel", ephemeral=True)
        return
    
    # get our stick manager to see if we have a stick active
    existing_stick = stick_manager.get_stick_by_channel(interaction.user.voice.channel)
    if existing_stick is None:
        log.log_info(f"Creating stick for {interaction.user.voice.channel.name} in {interaction.guild.name}")
        curr_stick = stick_manager.add_stick(interaction.user.voice.channel)
    else:
        curr_stick = existing_stick
    
    # claim the stick
    try:
        await curr_stick.claim(interaction)
        log.log_info(f"Claiming stick for {interaction.user.name} in {interaction.user.voice.channel.name}")
    except Exception as e:
        log.log_error(e)
        await interaction.response.send_message("Error claiming stick. Please try again later.\nIf the problem persists, contact an admin", ephemeral=True)
        log.log_warning(f"Due to error, deleting stick for {interaction.user.name} in {interaction.user.voice.channel.name}")
        stick_manager.del_stick(interaction.user.voice.channel)
        return

@bot.tree.command(name="tspass", description="Pass the talking stick.")
async def pass_stick(interaction: discord.Interaction):

    """
    Passes the talking stick.

    If the user doesn't have the stick, it will send a message indicating that.

    Parameters:
        interaction (discord.Interaction): The interaction object containing information about the command invocation and the user who invoked the command.

    Returns:
        None
    """
    # get our stick and pass
    curr_stick = stick_manager.get_stick_by_channel(interaction.user.voice.channel)
    if curr_stick is None:
        await interaction.response.send_message("There is no active talking stick!", ephemeral=True)
        return
    log.log_info(f"Passing stick for {interaction.user.name} in {interaction.user.voice.channel.name}")
    try:
        await curr_stick.pass_stick(interaction)
    except Exception as e:
        log.log_error(e)
        await interaction.response.send_message("Error passing stick. Please try again later.\nIf the problem persists, contact an admin", ephemeral=True)
        return

@bot.tree.command(name="help", description="Get help for the bot.")
async def print_help(interaction: discord.Interaction):
    """
    Get help for the bot.

    This command sends a message explaining how to use the bot and listing all the commands.
    """
    log.log_info(f"{interaction.user.name} used /help in {interaction.guild.name}")
    if check_admin(interaction.user):
        try:
            await interaction.response.send_message(
                "Talking Stick is a discord bot that allows you to have a talking stick session in a voice channel.\n"
                "To use the bot, claim the talking stick by typing /tsclaim. You must be in a voice channel.\n"
                "\nCommands:\n"
                "/tsclaim - Claim the talking stick\n"
                "/tspass - Pass the talking stick\n"
                "/enable - Enable the bot\n"
                "/disable - Disable the bot\n"
                "/settimeout - Set the timeout for the bot\n"
                "/help - Get help for the bot", 
                ephemeral=True
            )
            return
        except Exception as e:
            log.log_error(e)
            await interaction.channel.send("An error occurred while sending help.\nPlease try again, or contact an admin.")
    
    try:
        await interaction.response.send_message(
            "Talking Stick is a discord bot that allows you to have a talking stick session in a voice channel.\n"
            "To use the bot, claim the talking stick by typing /tsclaim. You must be in a voice channel.\n"
            "\nCommands:\n"
            "/tsclaim - Claim the talking stick\n"
            "/tspass - Pass the talking stick\n"
            "/help - Get help for the bot", 
            ephemeral=True
        )
    except Exception as e:
        log.log_error(e)
        await interaction.channel.send("An error occurred while sending help.\nPlease try again, or contact an admin.")



# --- Admin Commands ---

@bot.tree.command(name="enable", description="Enable the bot.")
@commands.has_permissions(administrator=True)
async def enable(interaction: discord.Interaction):
    """
    Enables the bot in the current server.

    This command is only available to server admins. If the user is not an admin, it will send a message indicating that.

    Parameters:
        interaction (discord.Interaction): The interaction object containing information about the command invocation and the user who invoked the command.

    Returns:
        None
    """
    log.log_info(f"{interaction.user.name} used /enable in {interaction.guild.name}")
    if check_admin(interaction.user):
        tsjson.enable_guild(interaction.guild)
        await interaction.response.send_message("The bot is now enabled for this server", ephemeral=True)
    else:
        await interaction.response.send_message("You are not an admin!", ephemeral=True)

@bot.tree.command(name="disable", description="Disable the bot.")
@commands.has_permissions(administrator=True)
async def disable(interaction: discord.Interaction):
    """
    Disables the bot in the current server.

    This command can only be executed by server administrators. It disables the bot for the server,
    ends any active talking stick sessions, and sends a confirmation message. If the user is not an
    administrator, it sends a message indicating lack of permissions.

    Parameters:
        interaction (discord.Interaction): The interaction object containing information about the
        command invocation and the user who invoked the command.

    Returns:
        None
    """
    log.log_info(f"{interaction.user.name} used /disable in {interaction.guild.name}")
    if not check_admin(interaction.user):
        # await interaction.response.send_message("You are not an admin!", ephemeral=True)
        print("You are not an admin!")
        return
    await interaction.response.send_message("The bot is now disabled for this server", ephemeral=True)
    tsjson.disable_guild(interaction.guild)
    await stick_manager.kill_sticks(interaction.guild)
    # await interaction.channel.send("The bot is now disabled for this server")
        

@bot.tree.command(name="settimeout", description="Set the timeout (in seconds) for the talking stick.")
@commands.has_permissions(administrator=True)
async def set_timeout(interaction: discord.Interaction, duration: int):
    """
    Sets the timeout for the talking stick in the current server.

    This command can only be executed by server administrators. It sets the timeout
    for the talking stick in the server, sends a confirmation message, and ends any
    active talking stick sessions. If the user is not an administrator, it sends a
    message indicating lack of permissions.

    Parameters:
        interaction (discord.Interaction): The interaction object containing
        information about the command invocation and the user who invoked the
        command.
        duration (int): The timeout duration in seconds.

    Returns:
        None
    """
    log.log_info(f"{interaction.user.name} used /settimeout in {interaction.guild.name}")
    if check_admin(interaction.user):
        tsjson.set_stick_timeout(interaction.guild, duration)
        await interaction.response.send_message(f"Timeout set to {duration} seconds", ephemeral=True)
    else:
        await interaction.response.send_message("You are not an admin!", ephemeral=True)

bot.run(TOKEN)