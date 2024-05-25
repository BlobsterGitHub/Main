import discord
import re
import sqlite3
from discord.ext import commands

# Set up the SQLite database
conn = sqlite3.connect('ip_user_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ip_user_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, username TEXT)''')
conn.commit()

# Define the bot and command prefix
intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Regex pattern to match the format !(IP) - [User]
pattern = re.compile(r'!\(([\d.]+)\) - \[(.+)\]')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    match = pattern.match(message.content)
    if match:
        ip = match.group(1)
        username = match.group(2)

        # Insert the data into the SQLite database
        c.execute("INSERT INTO ip_user_data (ip, username) VALUES (?, ?)", (ip, username))
        conn.commit()
        await message.channel.send(f'Data stored: IP={ip}, Username={username}')

    await bot.process_commands(message)

@bot.command(name='database')
async def fetch_database(ctx):
    c.execute("SELECT ip, username FROM ip_user_data")
    rows = c.fetchall()
    if rows:
        response = '\n'.join([f'IP: {row[0]}, Username: {row[1]}' for row in rows])
    else:
        response = 'The database is empty.'
    await ctx.send(response)

# Run the bot with your token
bot.run('MTIzMzQ2MDc3NTYwODEyNzU0Mg.G0L0HN.6gKQlNybWGVxpXgPuYFjHH6FUqFzuKWiFFP6zc')
