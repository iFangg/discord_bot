import discord, discord.ext, random, os, json
from discord.ext import commands, tasks
  
def checks(users, user):  
    if user not in users: #Checking if user is in database
        users[user] = {}
    if "pastry_number" not in users[user]: #different pastries
        users[user]["pastry_number"] = 0
        users[user]["pastries_baked"] = 0
        users[user]["trash"] = 0
        users[user]["delicious"] = 0
        users[user]["gourmet"] = 0
    if "balance" not in users[user]: #monies for user
        users[user]["balance"] = 0
