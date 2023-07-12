import Token
import random
import discord
import pandas as pd
from discord import app_commands
from discord.ext import commands
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer #,PorterStemmer
# from nltk.stem.snowball import SnowballStemmer
exec(open("Helpers/LoadData.py", encoding="utf8").read())
exec(open("Helpers/HelperFunctions.py", encoding="utf8").read())

bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    try:
        SyncSlashCommands = await bot.tree.sync()
        print(f"Synced {len(SyncSlashCommands)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.tree.command(name="chooseworkout", description="Randomly choose workout.")
async def sChooseWorkout(interaction: discord.Interaction):
    ExerciseOutput = fChooseExercise()
    await interaction.response.send_message(str("Hell yeah! Let's do " + ExerciseOutput.lower() + " today."))
    fWriteToLog(str(interaction.user.id), interaction.user.name,
                Mode = "/chooseworkout",
                Output = ExerciseOutput)

@bot.tree.command(name="help", description="I'll spot you, just ask \U0001F4AA")
async def sHelp(interaction: discord.Interaction):
    await interaction.response.send_message(fHelp(), ephemeral=True)
    fWriteToLog(str(interaction.user.id), interaction.user.name,
                Mode="/help",
                Output="Helpinfo")

@bot.tree.command(name="shutdown", description="Take me down, if you can")
async def sShutdown(interaction: discord.Interaction):
    if str(interaction.user.id) in Token.AdminID:  # Only admin can
        await interaction.response.send_message("You can't do that... I am invicib")
        fWriteToLog(str(interaction.user.id), interaction.user.name,
                    Mode="/shutdown",
                    Output="Success")
        await bot.close()
    else:
        await interaction.response.send_message("I'm sorry Dave, I'm afraid I can't do that")
        fWriteToLog(str(interaction.user.id), interaction.user.name,
                    Mode="/shutdown",
                    Output="Failure")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if fAddressesBeastBot(message.content):
        Response = fLoadMessageResponse(message.content)

        if Response['MessageType'] == 'text':
            await message.channel.send(Response['Output'])
            fWriteToLog(str(message.author.id), message.author.name,
                        Input = message.content,
                        Mode="Plaintext",
                        Output=Response['Output'])
        elif Response['MessageType'] == 'image':
            await message.channel.send(file=discord.File(Response['Output']))
            fWriteToLog(str(message.author.id), message.author.name,
                        Input=message.content,
                        Mode="Image",
                        Output=Response['Output'])


bot.run(Token.BotToken)
