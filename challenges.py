import asyncio
import random
import discord
from bot import bot
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from process_images import moderate_image

current_challenge = None
challenges = {}
submissions = {}
votes = {}

challenge_themes = [
    'Sunset',
    'Outer Space',
    'Futuristic City',
    'Underwater World',
    'Fantasy Landscape'
]

# Start a new challenge


async def start_challenge(ctx: discord.AppCommandContext, theme=None):
    global current_challenge

    if theme is None:
        theme = random.choice(challenge_themes)

    challenge_name = f'Drawing Contest - {theme}'

    challenges[challenge_name] = {
        'theme': theme,
        'start_time': datetime.now(),
        'end_time': datetime.now() + timedelta(hours=1),
        'submissions': [],
        'voting': False
    }

    submissions[challenge_name] = []
    votes[challenge_name] = {}

    current_challenge = challenge_name

    await ctx.send(f"New Challenge started! Theme: {theme}. You have 1 hour to submit your drawing!")
    await asyncio.sleep(3600)

    if len(challenges[challenge_name]['submissions']) >= 2:
        await end_challenge(ctx, theme)


# Command to start the challenge
@bot.command(name='start_challenge')
async def start_challenge_command(ctx, theme: str = None):
    await start_challenge(ctx, theme)


# Command to submit an entry (Image Submission)
@bot.command(name='submit')
async def submit(ctx):
    global current_challenge
    if current_challenge is None:
        await ctx.send("No active challenge. Please wait for a new one.")
        return

    challenge = challenges[current_challenge]
    if datetime.now() > challenge['end_time']:
        await ctx.send("The challenge is over. No more submissions can be made.")
        return

    # Check if the message has an attachment (image file upload)
    if len(ctx.message.attachments) > 0:
        image_url = ctx.message.attachments[0].url  # Get the image URL

        # Call moderate_image to check if the image is safe
        moderation_result = await moderate_image(image_url)

        if not moderation_result['is_safe']:
            await ctx.send(f"Your submission was flagged for inappropriate content: {moderation_result['reason']}")
            return

        # Add the image submission to the challenge
        challenge['submissions'].append({
            'user': ctx.author.name,
            'content': image_url
        })
        await ctx.send(f"Submission received from {ctx.author.name}!")

    else:
        # If no attachment is found, prompt the user to upload an image
        await ctx.send("Please submit an image by uploading a file.")

    # If there are 2 or more submissions, notify the user to end the challenge early
    if len(challenge['submissions']) >= 2:
        await ctx.send("There are enough submissions! Use !end_challenge to end the challenge early.")


# Command to end the challenge early
@bot.command(name='end_challenge')
async def end_challenge(ctx):
    global current_challenge
    challenge = challenges[current_challenge]

    if challenge['voting']:
        await ctx.send("Voting is already in progress.")
        return

    challenge['end_time'] = datetime.now()
    challenge['voting'] = True
    await ctx.send("The challenge is now closed! Voting will start shortly.")

    # Begin voting
    await start_voting(ctx)


# Voting period - 2 minutes to vote
async def start_voting(ctx):
    global current_challenge
    challenge = challenges[current_challenge]

    # Display submissions for voting
    submissions_list = "\n".join(
        [f"{idx+1}. {entry['user']} - {entry['content']}" for idx, entry in enumerate(challenge['submissions'])])
    await ctx.send(f"Time to vote! Here are the submissions:\n{submissions_list}\nReact with a number to vote for your favorite!")

    # Wait for 2 minutes (120 seconds)
    await asyncio.sleep(120)

    # Calculate winner based on votes
    winner = calculate_winner(ctx)
    await ctx.send(f"The winner is {winner['user']} with their submission: {winner['content']}!")
    current_challenge = None  # Reset current challenge


# Function to calculate the winner
def calculate_winner(ctx):
    global current_challenge
    challenge = challenges[current_challenge]

    # Tally votes
    vote_counts = {}
    for entry in challenge['submissions']:
        user = entry['user']
        if user not in vote_counts:
            vote_counts[user] = 0
        vote_counts[user] += 1

    # Determine the user with the most votes
    winner_user = max(vote_counts, key=vote_counts.get)
    winner = next(
        entry for entry in challenge['submissions'] if entry['user'] == winner_user)
    return winner


# Auto-schedule challenges every 3 hours
@tasks.loop(hours=3)
async def auto_challenge():
    if current_challenge is None:
        await start_challenge_command(bot, theme=None)

auto_challenge.start()
