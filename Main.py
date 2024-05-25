import discord
import re
import sqlite3
import shutil
from discord.ext import commands

# Set up the SQLite databases
conn_main = sqlite3.connect('ip_user_data.db')
conn_backup = sqlite3.connect('ip_user_data_backup.db')
c_main = conn_main.cursor()
c_backup = conn_backup.cursor()

# Create main table if not exists
c_main.execute('''CREATE TABLE IF NOT EXISTS ip_user_data
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, username TEXT)''')
conn_main.commit()

# Create backup table if not exists with the same structure as main
c_backup.execute('''CREATE TABLE IF NOT EXISTS ip_user_data
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, username TEXT)''')
conn_backup.commit()

# Define the bot and command prefix
intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Updated regex pattern to match the format !IP: [IP], Username: [Username]
pattern = re.compile(r'!IP: ([\d.]+), Username: (.+)')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)  # Process commands first

    print(f"Received message: {message.content}")  # Debugging output

    match = pattern.match(message.content)
    if match:
        ip = match.group(1)
        username = match.group(2)

        print(f"Matched IP: {ip}, Username: {username}")  # Debugging output

        # Check if the username already exists in the main database
        c_main.execute("SELECT * FROM ip_user_data WHERE username=?", (username,))
        existing_user = c_main.fetchone()

        if not existing_user:
            # Insert the data into the main SQLite database
            c_main.execute("INSERT INTO ip_user_data (ip, username) VALUES (?, ?)", (ip, username))
            conn_main.commit()
            await message.channel.send(f'Data stored: IP={ip}, Username={username}')
        else:
            await message.channel.send(f'Username {username} already exists in the main database.')

@bot.command(name='database-clear')
async def clear_database(ctx):
    c_main.execute("DELETE FROM ip_user_data")
    conn_main.commit()
    await ctx.send("Main database cleared.")

@bot.command(name='database-backup')
async def backup_database(ctx):
    try:
        shutil.copyfile('ip_user_data.db', 'ip_user_data_backup.db')
        await ctx.send("Database backup created successfully.")
    except Exception as e:
        await ctx.send(f"Failed to create database backup: {e}")

@bot.command(name='database-bv')
async def view_backup(ctx):
    try:
        conn_backup = sqlite3.connect('ip_user_data_backup.db')
        c_backup = conn_backup.cursor()

        # Fetch usernames and IPs from the backup database
        c_backup.execute("SELECT username, ip FROM ip_user_data")
        backup_data = c_backup.fetchall()

        if backup_data:
            response = '\n'.join([f'Username: {username}, IP: {ip}' for username, ip in backup_data])
        else:
            response = 'The backup database is empty.'

        await ctx.send(response)

        conn_backup.close()  # Close the backup database connection
    except Exception as e:
        await ctx.send(f"Failed to view backup database: {e}")

@bot.command(name='database')
async def fetch_database(ctx):
    c_main.execute("SELECT ip, username FROM ip_user_data")
    rows = c_main.fetchall()
    if rows:
        response = '\n'.join([f'IP: {row[0]}, Username: {row[1]}' for row in rows])
    else:
        response = 'The main database is empty.'
    await ctx.send(response)

@bot.command(name='bv-clear')
async def clear_backup(ctx):
    c_backup.execute("DELETE FROM ip_user_data")
    conn_backup.commit()
    await ctx.send("Backup database cleared.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        commands_list = [f"!{cmd.name}: {cmd.help}" for cmd in bot.commands]
        await ctx.send(f"Command not found. Did you mean any of these commands?\n\n'!database-bv' - Views the backup' \n'!database' - Views the database\n\nThose are the only public commands! ")

bot.run("MTI0Mzg4NzE2NzcxODAzNTUwNw.Gmn1mo.fK2EJ4dqFvw2ZsHU0GT39F0C2vDRbmMazvOLws")
