#discord,async,psutil,pyautogui,email,imaplib
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
    data = await accountdatabase_read_json()

    decklists = [i for i in data['accounts']]
    emails = [data['accounts'][i]['mail'] for i in data['accounts']]

    return decklists,emails

async def accountdatabase_read_json():
    with open(r'C:\Users\maxel\OneDrive\Skrivebord\mtg\accountdatabase.json', "r") as read_file:
        data = json.load(read_file)

    return data

async def read_ids(): #read ids
    with open(r'C:\Users\maxel\OneDrive\Skrivebord\mtg\idUses.json', "r") as read_file:
        data = json.load(read_file)

    return data

async def id_check(perm, id):
    data = await read_ids()

    sender_id = id

    registered_users = [str(i) for i in data] #all ids in databse

    #check if user id is registered
    if(str(sender_id) not in registered_users): #no user with id x present
        return None
    
    perm = data[str(sender_id)][perm] #perission to use new acc
    if(perm == False):
        return False
    else:
        return True

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
    perm = await id_check("account", sender_id) #redudant perm check,
    
    if(perm == False):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise Exception("Permission") #bad
    
    elif(perm == None):
        await interaction.response.send_message(f'Use /register to register an account.',ephemeral=True)
        raise Exception("No account present") #no account present
    else:
        pass #good

    decklists,emails = await get_decklists_emails()
    data = await accountdatabase_read_json()

    if(val not in decklists):
        await interaction.response.send_message("Provide a valid decklist",ephemeral=True)
    else:
        mail = data['accounts'][val]['mail']
        passw = data['accounts'][val]['pass']
        await interaction.response.send_message(f'Mail: {mail}\nPass: {passw}',ephemeral=True)


@bot.tree.command(name = "accounts", guild=MY_GUILD, description="all accounts in database")
async def get_decklists(interaction: discord.Interaction):
    sender_id = interaction.user.id
    perm = await id_check("accounts", sender_id)
    
    if(perm == False):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise Exception("Permission") #bad
    elif(perm == None):
        await interaction.response.send_message(f'Use /register to register an account.',ephemeral=True)
        raise Exception("No account present") #no account present
    else:
        pass #good
    
    decklists,emails = await get_decklists_emails()
    
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
    perm = await id_check("addaccount", str(sender_id))
    
    if(perm == False):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise Exception("Permission") #bad
    elif(perm == None):
        await interaction.response.send_message(f'Use /register to register an account.',ephemeral=True)
        raise Exception("No account present") #no account present
    else:
        pass #good

    decklists,emails = await get_decklists_emails()
    if(decklist in decklists):
        await interaction.response.send_message(f'No duplicate names',ephemeral=True)
        raise Exception("Duplicate name")
    
    if(mail in emails):
        await interaction.response.send_message(f'No duplicate emails',ephemeral=True)
        raise Exception("Duplicate email")
    
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
    data = await read_ids()
    sender_id = interaction.user.id

    #tries to acces databse, at id. if no id, catch error return /register
    try: #ugly code, fix later
        newacc_perm = data[str(sender_id)]['newaccount']['perm'] #perission to use new acc
    except:
        await interaction.response.send_message(f'Use /register to register an account.',ephemeral=True)
        raise Exception("No account present") #no account present
    
    if(newacc_perm == False):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise Exception("Permission") #bad
    else:
        if(data[str(sender_id)]['newaccount']['uses'] <= 0): #check for zeroes
            await interaction.response.send_message(f'You have zero uses left.',ephemeral=True)
            raise Exception("No more uses")
        
        else: #no zero eroor
            data[str(sender_id)]['newaccount']['uses'] += -1 #removes one use
            with open(r'C:\Users\maxel\OneDrive\Skrivebord\mtg\idUses.json', "w") as write_file:
                json.dump(data, write_file, indent=4)
            #pass
    
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
            data = await accountdatabase_read_json()
            seed = data['salt_seed']
            print(seed)
            print("\n\n")
            await interaction.edit_original_response(content=f'{str("<@" + str(sender_id) + ">")} Your account has been created\nAccount name: {usn}\nMail: {mail}\nPass: {passw}')
        except:
            await interaction.edit_original_response(content=f'please try again')
    #await interaction.response.send_message(f'Account created\nAccount name: {usn}\nMail: {mail}\nPass: {passw}',ephemeral=True)
    #await message.edit(content=f'{str("<@" + str(sender_id) + ">")} Your account created\nAccount name: {usn}\nMail: {mail}\nPass: {passw}')

@bot.tree.command(name = "backup", guild=MY_GUILD, description="returns a backup of all accounts")
async def new_account(interaction: discord.Interaction):
    sender_id = interaction.user.id
    perm = await id_check("backup", sender_id)
    
    if(perm == False):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise Exception("Permission") #bad
    elif(perm == None):
        await interaction.response.send_message(f'Use /register to register an account.',ephemeral=True)
        raise Exception("No account present") #no account present
    else:
        pass #good

    
    data = await accountdatabase_read_json()
    await interaction.response.send_message(f'{data}')

@bot.tree.command(name = "seed", guild=MY_GUILD, description="returns salt seed")
async def new_account(interaction: discord.Interaction):
    sender_id = interaction.user.id
    perm = await id_check("seed", sender_id)
    
    if(perm == False):
        await interaction.response.send_message(f'Not permitted',ephemeral=True)
        raise Exception("Permission") #bad
    elif(perm == None):
        await interaction.response.send_message(f'Use /register to register an account.',ephemeral=True)
        raise Exception("No account present") #no account present
    else:
        pass #good

    
    data = await accountdatabase_read_json()
    seed = data['salt_seed']
    await interaction.response.send_message(f'{seed}\n{bin(seed)}')

@bot.tree.command(name = "register", guild=MY_GUILD)
async def get_account(interaction: discord.Interaction):
    data = await read_ids()
    sender_id = interaction.user.id

    registered_users = [str(i) for i in data] #all ids in databse

    if(str(sender_id) in registered_users): #raise error if user is already present
        await interaction.response.send_message(f'You are already registered.',ephemeral=True)
        raise Exception('Already present')

    default_user = {
        sender_id : {
            "newaccount": {
                "perm": False,
                "uses": 0
            },

            "addaccount": False,
            "backup": False,
            "account" : True,
            "accounts" : True,
            "seed": False
        }
    }
    
    
    with open(r'C:\Users\maxel\OneDrive\Skrivebord\mtg\idUses.json', "r") as read_file:
        data = json.load(read_file)
    
    data[sender_id] = default_user[sender_id] #add user to data

    with open(r'C:\Users\maxel\OneDrive\Skrivebord\mtg\idUses.json', "w") as write_file:
        json.dump(data, write_file, indent=4)

    #send register message
    await interaction.response.send_message(f'You are now registered.',ephemeral=True)

if __name__ == '__main__':
    bot.run(token)
