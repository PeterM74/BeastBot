# BeastBot <img src="Data/BeastBotNoBG.png" align="right" height="150" width="150"/>
![](https://img.shields.io/badge/version-1.1.1-green)

BeastBot is a [Discord](https://discord.com/) bot for our gym group. He has a range of functions, including:

* Providing motivation images (silly AI-generated memes)
* Choosing a random workout and allow for exclusions if you want to skip leg day
* Will react to messages (based on other user's reactions)
* Optional integration with [InWorld.ai](https://inworld.ai/) large language model to create dynamic and flexible in-character responses, *OR*
* Very basic and limited compliment/insult system based on sentiment analysis

Best of all, he will stay out of your way unless you invoke one of his aliases in chat. Be aware that he can be rude and may not be appropriate for users <18.

# Getting started
Feel free to fork and host your own BeastBot. I am currently running him on a Raspberry Pi 2B (running Raspberry Pi OS) with minimal lag.

Firstly, fork and clone this repo onto your hosting platform. Next, you will need to generate a discord bot token - best to follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html).

Next, create an InWorld.ai character (optional - leave `UseInworldAIChatbot = False` if not). This is free provided you don't exceed 5000 API calls per month (very generous for a small-medium sized group) and is very simple to set up. Follow the instructions to generate your character, [source the API key](https://docs.inworld.ai/docs/tutorial-api/getting-started#authorization-signature) and workspace ID (by clicking on the 'More' option for your character). A character sheet is available in this repo if you wish to copy the options used for this project or feel free to make your own.

Take all these settings and create a `Settings.py` file in the root directory of the project with the following contents:

```python
BotToken = 'BOT_TOKEN_HERE'  # Paste token here
AdminID = ['YOUR_DISCORD_ID']  # Collect this from developer mode in Discord itself
# InWorld.AI settings
UseInworldAIChatbot = True  # Optional - set to false
## Only need to set the below if linking to InWorld
IW_WORKSPACE = 'workspaces/{WORKSPACE_ID}/characters/{CHARACTER_NAME}'
IW_APIURL = 'https://studio.inworld.ai/v1/' + IW_WORKSPACE + ':simpleSendText'
IW_APIKEYAuth = 'Basic {API_KEY_HERE}'
```

You will then need to install [Python](https://www.python.org/downloads/) and pip (usually comes packaged with Python). You will also need the libraries specified in `requirements.txt`. Run the `requirements.txt` file in the console:

```commandline
pip install -r requirements.txt
```

Next, in python, download some necessary data:

```python
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```

Every time you wish to change the slash commands that BeastBot uses, you will need to run the below to sync the commands to Discord. Note that there is a usage limit on this command so you should only run it once every few hours or it will be ignored.

```python
SyncSlashCommands = await bot.tree.sync()
```

Finally run the code in a terminal (e.g. `python BeastBotInitiator.py`) and [invite the bot](https://discordjs.guide/preparations/adding-your-bot-to-servers.html#creating-and-using-your-invite-link) to your server! If you see the message `Beasty is ready for action!` in your terminal, then it's working!

# LLM integration
The bot currently supports the use of the free InWorld.ai LLM to add conversational responses to BeastBot's other functions. While it is free and can hold a conversation, it is quite repetitive in it's responses (not surprising given it's purpose as a video game integration tool). I will add the ability to alternatively use ChatGPT instead.

## InWorld.ai examples

<img src="Data/InWorld BeastBot Screenshot1.jpg" width="300" height="303"/><img src="Data/InWorld BeastBot Screenshot2.jpg" width="348" height="303"/>

# Contributions
If you encounter a bug or crash, please file an [issue](https://github.com/PeterM74/BeastBot/issues) with a reproducible example if possible. You may also submit requests to improve the experience through the `enhancements` tag.

You are welcome to fork and submit a pull request. Ensure you update the `requirements.txt` file by running the below code after navigating to the root directory:

```commandline
pipreqs --encoding=utf8 . --force
```