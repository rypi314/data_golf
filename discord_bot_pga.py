import os
import json
import discord
from discord.ext import commands
import progress_timer
#print('wait 3 minutes for the data to load and app will stay online...')
#progress_timer.progress_bar(180)
import pga_matchup


# Grab token from config
with open("config.json") as f:
    config = json.load(f)
TOKEN = config["token"]

# Intents are required for certain activities
intents = discord.Intents.default()
intents.message_content = True

# Set up the bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

# data script 
df = pga_matchup.df_print

@bot.command(name='pga')
async def pga(ctx):
    await ctx.send(f'''Finding best tee time matchup for {pga_matchup.result_date}, from the world rankings.
                   {pga_matchup.df_print}
                   ''')

# Run the bot
bot.run(TOKEN)
