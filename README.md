# BeastBot <img src="Data/BeastBotNoBG.png" align="right" height="150" width="150"/>
![](https://img.shields.io/badge/version-1.0.1-green)

BeastBot is a [Discord](https://discord.com/) bot for our gym group. He has a range of functions, including:

* Providing motivation images (silly AI-generated memes)
* Choosing a random workout and allow for exclusions if you want to skip leg day
* Will react to messages (based on other user's reactions)
* Very basic and limited compliment/insult system based on sentiment analysis

Best of all, he will stay out of your way unless you invoke one of his aliases in chat. Be aware that he can be rude and may not be appropriate for users <18.

# Getting started
Feel free to fork and host your own BeastBot. I am currently running him on a Raspberry Pi 2B (running Raspberry Pi OS) with minimal lag.

Firstly, fork and clone this repo onto your hosting platform. Next, you will need to generate a bot token - best to follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html). Take this bot token and create a `Token.py` file in the root directory of the project with the following contents:

```python
BotToken = 'BOT_TOKEN_HERE'  # Paste token here
AdminID = ['YOUR_DISCORD_ID']  # Collect this from developer mode in Discord itself
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

Finally run the code and [invite the bot](https://discordjs.guide/preparations/adding-your-bot-to-servers.html#creating-and-using-your-invite-link) to your server!

# Contributions
If you encounter a bug or crash, please file an [issue](https://github.com/PeterM74/BeastBot/issues) with a reproducible example if possible. You may also submit requests to improve the experience through the `enhancements` tag.

You are welcome to fork and submit a pull request. Ensure you update the `requirements.txt` file by running the below code after navigating to the root directory:

```commandline
pipreqs --encoding=utf8 . --force
```