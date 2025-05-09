import discord
import asyncio
import src.stickq as stickq
# import src.config as config
import src.tsjson as tsjson
from time import sleep


class Stick:
    def __init__(self, channel: discord.VoiceChannel):
        
        """
        Initialize a new Stick object.

        Parameters
        ----------
        channel : discord.VoiceChannel
            The voice channel where the stick will be active.

        Attributes
        ----------
        timer_task : asyncio.Task
            The asyncio task that is responsible for changing the owner of the stick
            after a certain amount of time.
        active : bool
            Whether the stick is currently active.
        queue : set
            The set of users that are currently in the queue.
        channel : discord.VoiceChannel
            The voice channel where the stick is active.
        priv_thread : discord.Thread
            The private thread that is created for the users in the queue.
        """
        self.timer_task = None
        self.active = False
        self.queue = stickq.StickQueue()
        self.guild_id = channel.guild.id
        self.channel = channel
        self.priv_thread = None
<<<<<<< HEAD
=======
        self.super_stick = None
        self.emergency_used = []
>>>>>>> dev

    async def claim(self, interaction: discord.Interaction):
        """
        Claims the talking stick.

        If the user doesn't have the stick, it will add the user to the queue and send a message indicating their position in the queue.
        If the user already has the stick, it will send a message indicating that they already have the stick.
        If the bot is disabled, it will send a message indicating that the bot is disabled.

        Parameters:
            interaction (discord.Interaction): The interaction object containing information about the command invocation and the user who invoked the command.

        Returns:
            None
        """
        
        if not tsjson.is_guild_enabled(interaction.guild):
            await interaction.response.send_message("Bot disabled!", ephemeral=True)
            return

        member = interaction.user
        
<<<<<<< HEAD
        if self.active:
            self.queue.add(member)
            await interaction.response.send_message(f"You are number {self.queue.get_location()} in line", ephemeral=True)
            return
        
        self.queue.add(member)
=======
        self.queue.add(member, interaction)

        if self.active:
            await interaction.response.send_message(f"You are number {self.queue.get_location(member)} in line", ephemeral=True)
            return
        
>>>>>>> dev
        self.channel = member.voice.channel
        await self.start_session(interaction)
        self.active = True
        await interaction.response.send_message("Session started!", ephemeral=True)
<<<<<<< HEAD
        await self.priv_thread.send(f"{interaction.user.mention} has claimed the stick! You have {tsjson.get_stick_timeout(interaction.guild)} seconds to speak.")
        self.timer_task = asyncio.create_task(self.timeout_timer(interaction=interaction))
=======
        if tsjson.get_stick_timeout(interaction.guild) == 0:
            await self.priv_thread.send(f"{interaction.user.mention} has claimed the stick!")
        else:
            await self.priv_thread.send(f"{interaction.user.mention} has claimed the stick! You have {tsjson.get_stick_timeout(interaction.guild)} seconds to speak.")
            self.timer_task = asyncio.create_task(self.timeout_timer(interaction=interaction))
>>>>>>> dev
    
    async def pass_stick(self, interaction: discord.Interaction):
        """
        Passes the talking stick to the next user in queue.

        If no session is active, it sends a message indicating that. If the user
        attempting to pass the stick is not the first in the queue, it sends a 
        message indicating that they are not first in line. Otherwise, it removes 
        the user from the queue, unmutes the next user in line, and mutes the 
        current user. If the queue becomes empty, it ends the session.

        Parameters:
            interaction (discord.Interaction): The interaction object containing 
            information about the command invocation and the user who invoked the 
            command.

        Returns:
            None
        """
        if not self.active:
            await interaction.response.send_message("No session is active!", ephemeral=True)
            return

        member = interaction.user
<<<<<<< HEAD
        if member.id != self.queue.peek().id:
=======
        if member.id != self.queue.peek()["user"].id:
>>>>>>> dev
            await interaction.response.send_message("You are not the first in line!", ephemeral=True)
            return

        self.queue.pop()

<<<<<<< HEAD
        if self.queue.is_empty():
=======
        if self.queue.is_empty() and self.super_stick == None:
>>>>>>> dev
            if not interaction.response.is_done():
                await interaction.response.send_message("You passed the stick!", ephemeral=True)
            await self.end_session()
            return
        
<<<<<<< HEAD
        if self.timeout_timer:
            self.timeout_timer.cancel()
            self.timeout_timer = None

        next_member = self.queue.peek()
        # swap who is muted
        await next_member.edit(mute=False)
        await member.edit(mute=True)
        # restart timer
        self.timer_task = asyncio.create_task(self.timeout_timer(interaction=interaction))
=======
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
            self.timer_task = None

        next_member = self.queue.peek()["user"]
        next_member_interaction = self.queue.peek()["interaction"]
        # swap who is muted
        await next_member.edit(mute=False)
        if member != self.super_stick:
            await member.edit(mute=True)
        # restart timer
        self.timer_task = asyncio.create_task(self.timeout_timer(next_member_interaction))
>>>>>>> dev
        # finish up
        if not interaction.response.is_done():
            await interaction.response.send_message(f"You passed the stick.", ephemeral=True)
        await self.priv_thread.send(f"{next_member.mention} now has the stick!")

    async def start_session(self, interaction: discord.Interaction):      
        """
        Starts a talking stick session by muting all members in the channel 
        except the one who initiated the session.

        This function iterates over all members in the voice channel and mutes them 
        except for the user who invoked the command. It prepares the environment 
        for a talking stick session where only one person can speak at a time.

        Parameters:
            interaction (discord.Interaction): The interaction object containing 
            information about the command invocation and the user who invoked the 
            command.

        Returns:
            None
        """
        self.priv_thread = await interaction.channel.create_thread(name="Talking Stick Session", auto_archive_duration=60, type=discord.ChannelType.private_thread)
        for member in self.channel.members:
            await self.priv_thread.add_user(member)
<<<<<<< HEAD
            if member != interaction.user:
=======
            if member != interaction.user and member != self.super_stick:
>>>>>>> dev
                await member.edit(mute=True)
        
        await self.priv_thread.send("@everyone Talking Stick Session started! Use /tsclaim to claim the stick and /tspass to pass the stick.")
        
    async def end_session(self):
        """
        Ends a talking stick session.

        This function unmutes all members in the associated voice channel and sets the
        active status of the session to False.

        Returns:
            None
        """
<<<<<<< HEAD
        for member in self.channel.members:
            await member.edit(mute=False)
        self.active = False
        if self.timer_task:
            self.timer_task.cancel()
        await self.priv_thread.send(f"@everyone No one is queued for the stick! Session ending!")
        sleep(3)
        await self.priv_thread.delete()
=======
        print("ending")
        for member in self.channel.members:
            print(f"unmuting {member.name}")
            await member.edit(mute=False)
        self.active = False
        self.queue.clear()
        if self.timer_task:
            print("canceling timer")
            self.timer_task.cancel()
            self.timer_task = None
        print("sending message")
        await self.priv_thread.send(f"@everyone No one is queued for the stick! Session ending!") # <--------------------
        print("sleeping")
        sleep(3)
        print("deleting")  
        await self.priv_thread.delete()
        print("done")
>>>>>>> dev

    async def timeout_timer(self, interaction: discord.Interaction):
        """
        Starts a timeout timer for the current stick holder.

        This function waits for a duration specified by the configuration and then 
        sends a message to the private thread indicating that the current stick holder 
        has timed out. It subsequently passes the stick to the next user in the queue.

        Parameters:
            interaction (discord.Interaction): The interaction object containing 
            information about the command invocation and the user who invoked the 
            command.

        Returns:
            None
        """
<<<<<<< HEAD
        await asyncio.sleep(tsjson.get_stick_timeout(interaction.guild))
        await self.priv_thread.send(f"{interaction.user.mention} has timed out!")
        self.timeout_timer = None
        await self.pass_stick(interaction=interaction)
=======
        print("starting timer")
        timeout = tsjson.get_stick_timeout(interaction.guild)
        if timeout == 0:
            return
        await asyncio.sleep(timeout)
        await self.priv_thread.send(f"{interaction.user.mention} has timed out!")
        self.timer_task = None
        await self.pass_stick(interaction)

    async def assign_super_stick(self, member: discord.Member):

        if member.voice.channel != self.channel:
            return
        if self.super_stick is not None:
            await self.super_stick.edit(mute=False)
        if self.queue.get_location(member):
            self.queue.remove(member)
        self.super_stick = member
        
>>>>>>> dev

    async def handle_user_joining(self, member: discord.Member):
        """
        Handles a user joining the voice channel during an active session.

        If the session is active, this function sends a message to the private
        thread announcing that the member has joined, mutes the member, and adds
        them to the queue.

        Parameters:
            member (discord.Member): The member who joined the voice channel.

        Returns:
            None
        """
        if self.active:
            await self.priv_thread.add_user(member)
            await self.priv_thread.send(f"{member.mention} has joined the session!")
            await member.edit(mute=True)

    async def handle_user_leaving(self, member: discord.Member):
        """
        Handles a user leaving the voice channel during an active session.

        If the session is active, this function sends a message to the private
        thread announcing that the member has left, unmutes the member, and removes
        them from the queue.

        Parameters:
            member (discord.Member): The member who left the voice channel.

        Returns:
            None
        """
        if self.active:
<<<<<<< HEAD
            if member == self.queue.peek():
=======
            if member == self.queue.peek()["user"]:
>>>>>>> dev
                await self.pass_stick(member)
            await self.priv_thread.remove_user(member)
            await self.priv_thread.send(f"{member.mention} has left the session!")
            await member.edit(mute=False)
            self.queue.remove(member)

    async def kill_session(self):
        """
        Forcefully ends an active talking stick session.

        This function cancels any ongoing timer tasks, unmutes all members in the 
        associated voice channel, and marks the session as inactive. It also sends 
        a notification to the private thread about the session ending, waits for a 
        short duration, and deletes the private thread.

        Returns:
            None
        """

        if self.active:
            if self.timer_task:
                self.timer_task.cancel()
            self.active = False
            self.queue.clear()
            for member in self.channel.members:
                await member.edit(mute=False)
            await self.priv_thread.send(f"@everyone Session ended!")
            sleep(3)
            await self.priv_thread.delete()

    def __repr__(self):
<<<<<<< HEAD
        return f"Stick(active={self.active}, queue={self.queue}, channel={self.channel})"
=======
        return f"Stick(active={self.active}, queue={self.queue}, channel={self.channel}), guild_id={self.guild_id}, priv_thread={self.priv_thread}, timer_task={self.timer_task}"
>>>>>>> dev

class StickManager:
    def __init__(self):
        """
        Initializes the StickManager.

        This constructor creates an instance of the StickManager class, initializing
        an empty dictionary to store the active talking stick sessions, where the key
        is the voice channel ID and the value is the Stick instance associated with
        that channel.
        """
        self.sticks = {}
    
    def add_stick(self, channel: discord.VoiceChannel)  -> Stick:
        """
        Adds a talking stick session for the given voice channel to the manager.

        If the channel does not already have a talking stick session, this function
        initializes a new Stick instance for the channel and stores it in the dictionary
        of active sessions.

        Parameters:
            channel (discord.VoiceChannel): The voice channel to add a talking stick
            session for.
        """
        voice_channel_id = channel.id
        if voice_channel_id not in self.sticks:
            self.sticks[voice_channel_id] = Stick(channel)
            return self.sticks[voice_channel_id]

    def del_stick(self, channel: discord.VoiceChannel):
        """
        Deletes the talking stick session for the given voice channel from the manager.

        If the channel has an active talking stick session, this function removes
        it from the dictionary of active sessions.

        Parameters:
            channel (discord.VoiceChannel): The voice channel to delete the talking
            stick session for.
        """
        voice_channel_id = channel.id
        if voice_channel_id in self.sticks:
            del self.sticks[voice_channel_id]

    def purge_sticks(self) -> int:
        """
        Purges all active talking stick sessions from the manager.

        This function is used to clean up active sessions when the bot is shutting
        down. It removes all Stick instances from the dictionary of active sessions.

        Returns:
            int: The number of active sessions that were purged.
        """
        num_sticks_purged = 0
        for voice_channel_id in list(self.sticks):
            if not self.sticks[voice_channel_id].active:
                del self.sticks[voice_channel_id]
                num_sticks_purged += 1
        return num_sticks_purged
    
<<<<<<< HEAD
    def get_stick_by_channel(self, channel: discord.VoiceChannel):
=======
    def get_stick_by_channel(self, channel: discord.VoiceChannel) -> Stick:
>>>>>>> dev
        """
        Gets the talking stick session for the given voice channel from the manager.

        If the channel does not have an active talking stick session, this function
        returns None.

        Parameters:
            channel (discord.VoiceChannel): The voice channel to get a talking stick
            session for.

        Returns:
            Stick or None: The Stick instance for the given voice channel, or None if
            there is no active session.
        """
        voice_channel_id = channel.id
        return self.sticks.get(voice_channel_id)

    def get_sticks_by_guild(self, guild: discord.Guild):
        """
        Gets all talking stick sessions for the given guild from the manager.

        Parameters:
            guild (discord.Guild): The guild to get talking stick sessions for.

        Returns:
            list: A list of Stick instances for the given guild.
        """
        return [stick for stick in self.sticks.values() if stick.guild_id == guild.id]
    
    async def kill_sticks(self, guild: discord.Guild):
        """
        Ends all active talking stick sessions for the given guild.

        This function is used to shut down all active talking stick sessions in a
        guild when the bot is leaving the guild. It gets all active talking stick
        sessions for the guild and then calls the kill_session method on each of
        them.

        Parameters:
            guild (discord.Guild): The guild to end all active talking stick sessions
            for.
        """
        sticks = self.get_sticks_by_guild(guild)
        for stick in sticks:
            await stick.kill_session()
            self.del_stick(stick.channel)