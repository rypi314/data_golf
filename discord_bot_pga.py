import os
import json
import discord
from discord.ext import commands
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

@bot.command(name='pga')
async def pga(ctx):
    await ctx.send(f'''Hey {ctx.author.mention}
Finding best tee time matchup for {pga_matchup.result_date} according to the world rankings.
```{pga_matchup.markdown_table}```
                   ''')

# Run the bot
bot.run(TOKEN)
