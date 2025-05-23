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
            log.log_info('Syncing Commands...')
            await self.tree.sync()
            self.synced = True
        self.clear_sticks.start()
        log.log_info('Done!')
    
    

    async def on_ready(self):
        await self.change_presence(activity=discord.CustomActivity("Use /help"))
        log.log_info(f'{self.user} has connected to Discord!')

bot = bot(intents=intents)
stick_manager = ts.StickManager()


# --- Utilities ---

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

def check_thread_permissions(channel: discord.TextChannel, users: list[discord.User]) -> bool:
    """
    Checks if all users in a list have permissions to view a given text channel.

    This function iterates over the users in the list and checks if they have the
    'view_channel' permission for the given text channel. If any of the users do
    not have this permission, the function returns False. If all users do have
    this permission, the function returns True.

    Parameters:
        channel (discord.TextChannel): The text channel to check.
        users (list[discord.User]): The users to check.

    Returns:
        bool: True if all users have permissions to view the channel, False otherwise.
    """
    for user in users:
        if not channel.permissions_for(user).send_messages:
            return False
    return True

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
    # User joins a voice channel with active stick
    if before.channel != after.channel and after.channel is not None:
        existing_stick = stick_manager.get_stick_by_channel(after.channel)
        if existing_stick is not None:
            try:
                await existing_stick.handle_user_joining(member)
                log.log_info(f"{member.name} joined {after.channel.name}")
            except Exception as e:
                log.log_error(e)
                member.send("An error occurred while joining the session.\nThe most likely cause is that you don't have permissions for the text channel in which the session was called from.\nPlease try again, or contact an admin.")
    # User leaves a voice channel with active stick
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
    
    # Check if all users in call have access to the text channel that the command was invoked in
    if not check_thread_permissions(interaction.channel, interaction.user.voice.channel.members):
        await interaction.response.send_message("ERROR:\nNot everyone in your call has access to this text channel. Please use a text channel that everyone has access to.", ephemeral=True)
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
<<<<<<< HEAD
=======
        curr_stick.kill_session()
>>>>>>> dev
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
    # no active stick for this call
    if curr_stick is None:
        await interaction.response.send_message("There is no active talking stick!", ephemeral=True)
        return
    log.log_info(f"Passing stick for {interaction.user.name} in {interaction.user.voice.channel.name}")
    # pass
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

    # Admin commands
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
    
    # User commands
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

<<<<<<< HEAD


# --- Admin Commands ---

=======
# --- Admin Commands ---

# @bot.tree.command(name="super", description="Grants a user a super stick.")
# @commands.has_permissions(administrator=True)
# async def super_stick(interaction: discord.Interaction, user: discord.User):
#     """
#     Grants a user a super stick.

#     This command is only available to server admins. If the user is not an admin, it will send a message indicating that.

#     Parameters:
#         interaction (discord.Interaction): The interaction object containing information about the command invocation and the user who invoked the command.
#         user (discord.User): The user to grant a super stick to.

#     Returns:
#         None
#     """
#     log.log_info(f"{interaction.user.name} used /super in {interaction.guild.name}")
#     existing_stick = stick_manager.get_stick_by_channel(interaction.user.voice.channel)
#     if existing_stick is None:
#         await interaction.response.send_message("There is no active talking stick!", ephemeral=True)
#         return
    
#     if check_admin(interaction.user):
#         existing_stick.assign_super_stick(user)
#         await interaction.response.send_message(f"Super stick granted to {user.name}", ephemeral=True)
#     else:
#         await interaction.response.send_message("You are not an admin!", ephemeral=True)

>>>>>>> dev
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
        await interaction.response.send_message("You are not an admin!", ephemeral=True)
        return
    await interaction.response.send_message("The bot is now disabled for this server", ephemeral=True)
    tsjson.disable_guild(interaction.guild)
    await stick_manager.kill_sticks(interaction.guild)
        

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