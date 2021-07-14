import discord, discord.ext, random, os, json
import Pchecks as checks
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.default() # Enable all intents except for members and presences
intents.members = True  # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix = "p!", intents = intents) 
pastry = "pastries.json"
prefixJ = "p_prefixes.json"



def get_prefix(bot, message):
    try:
        with open(prefixJ, 'r') as f:
            prefixes = json.load(f)
            return prefixes[str(message.guild.id)]
        
    except KeyError: # if the guild's prefix cannot be found in 'p_prefixes.json'
        with open(prefixJ, 'r') as k:
            prefixes = json.load(k)
        prefixes[str(message.guild.id)] = 'p!'

        with open(prefixJ, 'w') as j:
            json.dump(prefixes, j, indent = 4)

        with open(prefixJ, 'r') as t:
            prefixes = json.load(t)
            return prefixes[str(message.guild.id)]
    
bot = commands.Bot(command_prefix = get_prefix)

bot.remove_command('help')

@bot.command(pass_context = True, aliases = ['Help'])
async def help(ctx, dm = None):
    author = ctx.message.author

    embed = discord.Embed(
        colour = 0xFFF8F6
    )

    embed.set_author(name = 'Help')
    embed.add_field(name = 'Bake', value = 'Bake some pastries', inline = False)
    embed.add_field(name = 'Feed', value = 'Feed someone with your pastries')
    embed.add_field(name = 'Bet', value = 'Bet your money (from baking delicious pastries) in games such as coinflip\nuse: p!bet bet_type(i.e coinflip AMOUNT)')
    embed.add_field(name = 'Donate', value = 'Help a brother out with some donations')
    embed.add_field(name = 'Leaderboard', value = 'Check who\'s atop of the pastry and money leaderboards\nusage: p!leaderboard pastry/balance', inline = False)
    await ctx.send (embed = embed)

    if dm != None:
        await author.send(embed = embed)
        await ctx.send("Check DM's")

@bot.command
@commands.has_permissions(administrator = True)
async def prefix(ctx, prefix):
    with open(prefix, "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("p_prefixes.json", "w") as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(f"Prefix has been changed to: {prefix}")
    

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game('p!help'))
    print("Ready to *serve* pastry puffs") #LOL
    

@bot.command(aliases = ['Bake'])
@commands.cooldown(1, 2.5, type = commands.BucketType.user)
async def bake(ctx): #id into file
    with open(pastry, "r") as f:
        users = json.load(f) #file things      
    user = str(ctx.author.id)
    checks.checks(users, user) #checking if user is in database
    pastries = ["Raisin pastry", "Sour bread", "White bread pastry", "Banana bread"]
    unlockables = ["Blueberry muffin", "Chocolate chip cookie", "Classic cake"]
    adjectives = ["burnt", "disgusting", "soggy", "GROT", "weirdchamp", "inedible", "homophobic", "sacrilegious", "foul", "beastly"]
    users[user]["pastry_number"] += 1
    users[user]["pastries_baked"] += 1  
    if 5 < random.randint(1, 1000) < 50:
        if users[user]["pastries_baked"] >= 10:
            embed = discord.Embed(description = f"{ctx.author.mention}, You have made a delicious {random.choice(pastries, unlockables)}! Check your balance.\nTotal pastries made: {users[user]['pastry_number']}", colour = 0xc68958)
            await ctx.send(embed = embed)
            users[user]["delicious"] += 1
            users[user]["balance"] += 10            
        embed = discord.Embed(description = f"{ctx.author.mention}, You have made a delicious {random.choice(pastries)}! Check your balance.\nTotal pastries made: {users[user]['pastry_number']}", colour = 0xFFFFFF)
        await ctx.send(embed = embed)
        users[user]["delicious"] += 1
        users[user]["balance"] += 10 
    elif random.randint(1, 1000) <= 5:
        embed = discord.Embed(description = f"{ctx.author.mention}, You have made a Gourmet 5 Michelin Star {random.choice(pastries)}!\nTotal pastries made: {users[user]['pastry_number']}", colour = 0xFFDF00)
        await ctx.send(embed = embed)
        await ctx.message.author.send("You actually made something worthy, have something for your efforts.\nCheck your balance.")
        users[user]["gourmet"] += 1
        users[user]["balance"] += 100
    else:
        embed = discord.Embed(description = f"{ctx.author.mention}, You have made a {random.choice(adjectives)} {random.choice(pastries)}!\nTotal pastries made: {users[user]['pastry_number']}", colour = 0xc68958)
        await ctx.send(embed = embed)
        users[user]["trash"] += 1
            
    
    with open(pastry, "w") as f:
        f.write(json.dumps(users, indent=5))

@bot.command()
async def feed(ctx, member : discord.Member, amount = 1): #feed  people
    user = str(ctx.author.id)
    member = str(member.id)
    counter = amount
    with open(pastry, "r") as f:
        users = json.load(f) #file things   
    checks.checks(users, user)
    checks.checks(users, member)                            
    if users[user]["pastry_number"] < amount or amount < 0: #checking if user has enough pastries
        embed = discord.Embed(description = f"You have no pastry puffs. Type ‘p!bake’ to make some.", colour = 0xFFFFFF)
        return await ctx.send(embed = embed)
    else:            
        users[user]["pastry_number"] -= amount #taking pastries from user
        while users[user]["trash"] > 0 and counter > 0: #do they have enough trash pastries?
            users[user]["trash"] -= 1 
            counter -= 1
            if users[user]["trash"] <= 0 and counter > 0: #if not we take their pastries actually worth something
                while users[user]["delicious"] > 0 and counter > 0:  
                    users[user]["delicious"] -= 1
                    counter -= 1
                if users[user]["delicious"] <= 0 and counter > 0:
                    while users[user]["gourmet"] > 0 and counter > 0:  
                        users[user]["gourmet"] -= 1
                        counter -= 1
        embed = discord.Embed(description = f"{ctx.author.mention} has fed <@{member}> {amount} pastries!", colour = 0xFFFFFF)
        await ctx.send(embed = embed)
    with open(pastry, "w") as f:
        f.write(json.dumps(users, indent=5))

@bot.command()
async def pantry(ctx, member : discord.Member = None):
    with open(pastry, "r") as f:
        users = json.load(f)
    if member == None:
        member = ctx.author    
    user = str(member.id)
    checks.checks(users, user)
    if users[user]['gourmet'] > 0:
        await ctx.send(embed = discord.Embed(title = f'{member.name}\'s pastries:', description = f"Total pastries: {users[user]['pastry_number']}\nTrash pastries: {users[user]['trash']}\nDelicious pastries: {users[user]['delicious']}\nGourmet Pastries: {users[user]['gourmet']}", colour = 0xFFDD00))
    else:
        await ctx.send(embed = discord.Embed(title = f'{member.name}\'s pastries:', description = f"Total pastries: {users[user]['pastry_number']}\nTrash pastries: {users[user]['trash']}\nDelicious pastries: {users[user]['delicious']}\nGourmet Pastries: {users[user]['gourmet']}", colour = 0xFFFFFF))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Stop being impatient - {error.retry_after % 60:,.1f}s left")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Not command??? p!help to see available commands.")
    else:
        raise error 

@bot.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    bot.load_extension(f"Pcogs.{extension}")
    await ctx.send(f"{extension} has been loaded")

@bot.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    bot.unload_extension(f"Pcogs.{extension}")
    await ctx.send(f"{extension} has been unloaded")

@bot.command()
@commands.has_permissions(administrator = True)
async def reload(ctx, extension):
    bot.unload_extension(f"Pcogs.{extension}")
    bot.load_extension(f"Pcogs.{extension}")
    await ctx.send(f"{extension} has been reloaded")

for filename in os.listdir("./Pcogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Pcogs.{filename[:-3]}") 

bot.run("TOKEN")
