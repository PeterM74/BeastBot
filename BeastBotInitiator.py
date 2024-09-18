import Settings
import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio
from openai import OpenAI
from Helpers.HelperFunctions import *

# Initialise Session ID if using InWorld API integration
## Leave blank as it will be overwritten on first call to API
CurrentSessionID = ''

bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print("Beasty is ready for action!")
    # SyncSlashCommands = await bot.tree.sync()


@bot.tree.command(name="chooseworkout", description="Randomly choose workout.")
async def sChooseWorkout(interaction: discord.Interaction):
    ExerciseOutput = fChooseExercise()
    await interaction.response.send_message(str("Hell yeah! Let's do " + ExerciseOutput.lower() + " today."))

@bot.tree.command(name="generateimage", description="Generate an image by description.")
async def sGenerateImage(interaction: discord.Interaction, description: str):
    # There is 3s response time before timeout
    await interaction.response.defer()
    ResponseURL = await fRequestDALLE(description)
    # await interaction.response.send_message(ResponseURL)
    await interaction.followup.send(content=ResponseURL)

@bot.tree.command(name="help", description="I'll spot you, just ask \U0001F4AA")
async def sHelp(interaction: discord.Interaction):
    await interaction.response.send_message(fHelp(), ephemeral=True)

@bot.tree.command(name="shutdown", description="Take me down, if you can")
async def sShutdown(interaction: discord.Interaction):
    if str(interaction.user.id) in Settings.AdminID:  # Only admin can
        await interaction.response.send_message("You can't do that... I am invicib")
        await bot.close()
    else:
        await interaction.response.send_message("I'm sorry Dave, I'm afraid I can't do that")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if fAddressesBeastBot(message.content):
        # Concatenate messages that are sent together in a short timespan
        MessageHistoryObj = bot.get_channel(message.channel.id).history(limit=10)
        MessageHistoryList = [message async for message in MessageHistoryObj][::-1]  # Last message first

        GroupedMessageString = await fCycleThroughMessageFormatting(MessageHistoryList, message)

        Response = await fLoadMessageResponse(message.content, # Does this need to be run through Vision too?
                                              GroupedMessageString,
                                              message.author.name,
                                              CurrentSessionID)

        if Response['MessageType'] == 'text':
            await message.channel.send(Response['Output'])
        elif Response['MessageType'] == 'image':
            await message.channel.send(file=discord.File(Response['Output']))

@bot.event
async def on_raw_reaction_add(payload):
    MessageReceived = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if MessageReceived.author == bot.user:
        return

    await MessageReceived.add_reaction(payload.emoji)


bot.run(Settings.BotToken)
