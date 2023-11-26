import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import json

from wiz import create_account

token = 'token' #mtg bot

client = discord.Client(intents = discord.Intents.all())

bot = commands.Bot(command_prefix='$',intents = discord.Intents.all())
MY_GUILD = discord.Object(id=1177735119738519552)

async def get_decklists_emails():
    with open("accountdatabase.json", "r") as read_file:
        data = json.load(read_file)

    decklists = [i for i in data['accounts']]
    emails = [data['accounts'][i]['mail'] for i in data['accounts']]

    return decklists,emails

async def read_json():
    with open("accountdatabase.json", "r") as read_file:
        data = json.load(read_file)

    return data

valid_user_id = [937017841356505278,972980724951040051] #lunamowon, plsnt

@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await bot.tree.sync(guild=MY_GUILD)
        print(len(synced))
    except Exception as e:
        print(e)

@bot.tree.command(name = "account", guild=MY_GUILD)
@app_commands.describe(val = "Which deck do you want? ")
async def get_account(interaction: discord.Interaction, val: str):
    sender_id = interaction.user.id

    decklists,emails = await get_decklists_emails()
    data = await read_json()

    if(val not in decklists):
        await interaction.response.send_message("Provide a valid decklist",ephemeral=True)
    else:
        mail = data['accounts'][val]['mail']
        passw = data['accounts'][val]['pass']
        await interaction.response.send_message(f'Mail: {mail}\nPass: {passw}',ephemeral=True)


@bot.tree.command(name = "accounts", guild=MY_GUILD, description="all accounts in database")
async def get_decklists(interaction: discord.Interaction):
    decklists,emails = await get_decklists_emails()
    discord_id = interaction.user.id
    
    msg_str = ''
    for i in range(len(decklists)):
        msg_str += f'{i+1}) {decklists[i]}\n'
    await interaction.response.send_message(str(msg_str),ephemeral=True)

@bot.tree.command(name = "addaccount", guild=MY_GUILD)
@app_commands.describe(decklist= "Name of deck: ")
@app_commands.describe(mail = "Mail: ")
@app_commands.describe(passw = "Password: ")
async def get_account(interaction: discord.Interaction, mail: str, passw: str, decklist: str):
    sender_id = interaction.user.id
    decklists,emails = await get_decklists_emails()

    if(sender_id not in valid_user_id):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise ValueError
    
    if(decklist in decklists):
        await interaction.response.send_message(f'No duplicate names',ephemeral=True)
        raise ValueError
    
    if(mail in emails):
        await interaction.response.send_message(f'No duplicate emails',ephemeral=True)
        raise ValueError
    
    account_dict = {
        decklist : {
            "mail" : mail,
            "pass" : passw
        }
    }

    with open("accountdatabase.json", "r") as read_file:
        data = json.load(read_file)
    
    data['accounts'][decklist] = account_dict[decklist]

    with open("accountdatabase.json", "w") as write_file:
        json.dump(data, write_file, indent=4)

    await interaction.response.send_message(f'Account added\nMail: {mail}\nPass: {passw}\nName: {decklist}')
    #await interaction.response.send_message(f'{account_dict}',ephemeral=True)


command_locks = {}
@bot.tree.command(name = "newacc", guild=MY_GUILD, description="create a new account\ntakes 1 minute")
async def new_account(interaction: discord.Interaction):
    sender_id = interaction.user.id
    if(sender_id not in valid_user_id):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise ValueError
    
    # Get or create a lock for this command
    lock = command_locks.get('example', None)
    if not lock:
        lock = asyncio.Lock()
        command_locks['example'] = lock

    async with lock:
        await interaction.response.send_message("Making account please wait for 1m")
        
        try:
            mail, passw, usn = await create_account("Cool Cat", lock=asyncio.Lock()) #redudant lock will fix later
            print(mail,passw,usn)
            await interaction.edit_original_response(content=f'{str("<@" + str(sender_id) + ">")} Your account has been created\nAccount name: {usn}\nMail: {mail}\nPass: {passw}')
        except:
            await interaction.edit_original_response(content=f'please try again')
    #await interaction.response.send_message(f'Account created\nAccount name: {usn}\nMail: {mail}\nPass: {passw}',ephemeral=True)
    #await message.edit(content=f'{str("<@" + str(sender_id) + ">")} Your account created\nAccount name: {usn}\nMail: {mail}\nPass: {passw}')

@bot.tree.command(name = "backup", guild=MY_GUILD, description="returns a backup of all accounts")
async def new_account(interaction: discord.Interaction):
    sender_id = interaction.user.id
    if(sender_id not in valid_user_id):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise ValueError
    
    data = await read_json()
    await interaction.response.send_message(f'{data}')
    
if __name__ == '__main__':
    bot.run(token)
