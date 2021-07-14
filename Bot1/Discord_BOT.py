import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
import os
import json

prefix = "prefixes.json"

def get_prefix(client, message):
    with open(prefix, "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
statuses = cycle([".help", ".8ball"])

client.remove_command('help')

@client.event
async def on_ready():
    change_status.start()
    print("Bot is pog")

@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = 0xE0115F
    )

    embed.set_author(name = 'Help')
    embed.add_field(name = 'Ping', value = 'Returns Pong! and latency', inline = False)
    embed.add_field(name = '8ball', value = 'Ask a question and get an answer', inline = False)
    await author.send(embed = embed)
    await ctx.send("Check DM's")

@client.event
async def on_guild_join(guild):
    with open(prefix, "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."

    with open(prefix, "w") as f:
        json.dump(prefixes, f, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open(prefix, "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open(prefix, "w") as f:
        json.dump(prefixes, f, indent = 4)

@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):
    with open(prefix, "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open(prefix, "w") as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(f"Prefix has been changed to: {prefix}")

@client.event
async def on_command_error(ctx, error):
    prefix = "prefixes.json"
    with open(prefix, "r") as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"? {prefix}help to see available commands")
    else:
        print(error)

@client.event
async def check_failure_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to do that")
    else:
        print(error)

@tasks.loop(seconds = 3600)
async def change_status():
    await client.change_presence(
    activity = discord.Game(next(statuses)), status = discord.Status.dnd)

@client.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} has been loaded")

@client.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} has been unloaded")

@client.command()
@commands.has_permissions(administrator = True)
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} has been reloaded")

@client.event
async def on_member_join(member):
    print(f"{member} has joined")

@client.event
async def on_member_remove(member):
    print(f"{member} has been evicted")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 5 ):
    confirmation = ['yes', 'no']
    if amount >= 50:
        await ctx.send("Are you sure?")

        def check(message):
          return message.author == ctx.author

        amsure = await client.wait_for("message", check=check, timeout=30.0)
        print(f"{ctx.author} said \"{amsure.content}\" and did/did not clear {amount} lines")
        if amsure.content not in confirmation:
            await ctx.send("??? We'll try this again, Are you sure?")
            def check(message):
                return message.author == ctx.author
                
        elif amsure.content == "yes":
            await ctx.channel.purge(limit = amount + 3)
        else:
            await ctx.send("monkaS")
    else:
        await ctx.channel.purge(limit = amount + 1)



@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing Amount to Clear!")
    else:
        raise error


@client.command()
@commands.has_permissions(administrator = True)
async def punish(ctx, member : discord.Member, action = "kick", *, reason=None):
    if action == "kick":
        await member.kick(reason=reason)
        await member.send("lmao")
        await member.send("🤸‍♂️\n\n\n\n                                    🦽🏌️")
        await ctx.send(f"Kicked {member}")
        await ctx.send("🤸‍♂️\n\n\n\n                                    🦽🏌️‍♂️")
    elif action == "ban":
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member}")

@client.command()
async def icon(ctx, member : discord.Member):
    await ctx.send(embed=discord.Embed(
    title=f"{member.name}'s avatar").set_image(url=member.avatar_url))

#@client.event
#async def on_typing(channel, user, when):
     #await message.channel.trigger_typing(f"{str(user)} is typing at {str(channel)} in this time: {str(when)}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run("Njk1Nzg2OTg1ODY4MjMwNjY2.XofQIA.ybw8m4e63QC41pF7v4bcnOjfoWY")
