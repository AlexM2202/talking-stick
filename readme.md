<a href="https://www.buymeacoffee.com/clipt" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>


**Discord Talking Stick Bot**
=============================================

A fun and interactive Discord bot that helps you manage conversations in your voice channels!

What is it?

The Talking Stick Bot is a virtual "talking stick" that allows only one person to speak at a time in a voice channel. It's perfect for large groups, meetings, or discussions where you want to ensure everyone gets a chance to contribute without interruptions.

**Features**
------------

*   Allows users to claim and pass a virtual "talking stick" in a voice channel
*   Automatically mutes and unmutes users as they claim and pass the stick
*   Supports multiple talking stick sessions across different voice channels
*   Includes a help command with instructions on how to use the bot
*   Supports admin-only commands for enabling, disabling, and setting timeouts for the bot

**Getting Started**
---------------
To use the Talking Stick, you can invite the bot to your discord server using the invite link [here](https://discord.com/oauth2/authorize?client_id=1253826844436856944). If you want to host the bot yourself follow the self hosting guide below.


**Self-Hosting**
----------------

To self-host the Talking Stick bot, follow these steps:

1.  Create a discord bot
    Navigate to the Discord Developer Portal [here](https://discord.com/login?redirect_to=/developers) and create a discord bot. In the 'Installation' tab make sure that 'Guild Install' is selected. In the 'Scopes' Select 'bot' and 'applications.commands'. Next make sure you have the following permissions selected
    * Create Private Threads
    * Manage Threads
    * Mention Everyone
    * Mute Members
    * Send Messages
    * Send Messages in Threads
    * Use Voice Activity
    * View Channels
    Once you have those selected copy the Install Link and paste it into any browser, or into a text channel in the server you want to install the bot in.

    Finally, navigate to the 'Bot' tab and click 'Reset Token'. Discord will prompt you for your password, after entering it it will show a token on screen. Copy it and save it for later. We will use it during the install.

2.  Clone the repository:
    ```bash
        git clone https://github.com/your-username/talking-stick-bot.git
    ```
3.  Navigate to the `talking-stick` directory:
    ```bash
        cd talking-stick
    ```
4.  Run the installation script:
    ```bash
        bash install.sh
    ```
This script will install the required dependencies, create a virtual environment, and set up the bot.
5.  Set up your bot token:
    * Use the API token that we got when we created our discord bot and paste it into the terminal when prompted
    ```bash
        Enter your bot token: 
    ```

Note, this bot was intended to run on linux systems. I cannot confirm it will work on Windows based machines.


**Running the Bot**
-------------------

To run the bot, navigate to the `talking-stick` directory and run the following command:
```bash
bash start.sh
```
This script will activate the virtual environment and start the bot. To stop it use CTRL+C.


**Whats Next**
-------------------

* Super Stick - if a user has a super stick they will not be muted during the session
* Dump Queue - a fast command what will dump the queue and end the session (a kill switch)

Love using the Talking Stick Bot? Consider buying me a coffee to support its development and maintenance! [here](https://buymeacoffee.com/clipt)

**Troubleshooting**
-------------------

*   If you encounter any issues while running the bot, check the `logs` directory for error messages.
*   If you need help or have questions, feel free to open an issue on the GitHub repository.


**License**
------------

The Talking Stick bot is licensed under the [MIT License](https://opensource.org/licenses/MIT).