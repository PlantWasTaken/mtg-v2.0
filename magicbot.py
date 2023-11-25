import discord
from discord import app_commands
from discord.ext import commands
import json

from wiz import create_account



client = discord.Client(intents = discord.Intents.all())

bot = commands.Bot(command_prefix='$',intents = discord.Intents.all())
MY_GUILD = discord.Object(id=1177735119738519552)

def get_decklists_emails():
    with open("accountdatabase.json", "r") as read_file:
        data = json.load(read_file)

    decklists = [i for i in data['accounts']]
    emails = [data['accounts'][i]['mail'] for i in data['accounts']]

    return decklists,emails

def read_json():
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

    decklists,emails = get_decklists_emails()
    data = read_json()

    if(val not in decklists):
        await interaction.response.send_message("Provide a valid decklist",ephemeral=True)
    else:
        mail = data['accounts'][val]['mail']
        passw = data['accounts'][val]['pass']
        await interaction.response.send_message(f'Mail: {mail}\nPass: {passw}',ephemeral=True)


@bot.tree.command(name = "accounts", guild=MY_GUILD, description="all accounts in database")
async def get_decklists(interaction: discord.Interaction):
    decklists,emails = get_decklists_emails()
    discord_id = interaction.user.id
    
    await interaction.response.send_message(str(decklists),ephemeral=True)

@bot.tree.command(name = "addaccount", guild=MY_GUILD)
@app_commands.describe(decklist= "Name of deck: ")
@app_commands.describe(mail = "Mail: ")
@app_commands.describe(passw = "Password: ")
async def get_account(interaction: discord.Interaction, mail: str, passw: str, decklist: str):
    sender_id = interaction.user.id
    decklists,emails = get_decklists_emails()

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

    await interaction.response.send_message(f'Account added\nMail: {mail}\nPass: {passw}\nName: {decklist}',ephemeral=True)
    #await interaction.response.send_message(f'{account_dict}',ephemeral=True)

@bot.tree.command(name = "newacc", guild=MY_GUILD, description="create a new account")

async def new_account(interaction: discord.Interaction):
    sender_id = interaction.user.id
    if(sender_id not in valid_user_id):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise ValueError
    
    
    await interaction.response.send_message(f'asd',ephemeral=True)
bot.run(token)