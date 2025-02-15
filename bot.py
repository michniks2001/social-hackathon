import discord
import os

from discord.ext import commands
from load_dotenv import load_dotenv
from toxicity_analysis import predict_toxicity_and_sarcasm

load_dotenv()

TOKEN = os.environ.get("DISCORD_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    toxicity_levels = predict_toxicity_and_sarcasm(message)

    if toxicity_levels['toxicity_level'] >= 8:
        if toxicity_levels['sarcasm_level'] < 3:
            await message.delete()
            await message.channel.send('Watch your mouth!')
    else:
        pass

    await bot.process_commands(message)

#

if TOKEN:
    bot.run(TOKEN)
else:
    raise Exception("Invalid token or token not found!")
