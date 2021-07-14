import discord, random, json
from discord import Embed
from discord.ext import commands

class Rankings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    intents = discord.Intents.default()
    intents.members = True
    
    # Global leaderboard (Currently)
    @commands.command(aliases = ['lb', 'Leaderboard', 'LB', 'Lb'])
    async def leaderboard(self, ctx, rankings = "pastry", lb_no = 3):
        value = "pastry_number"
        if rankings.lower() == "pastry":
            value = "pastry_number"
        elif rankings.lower() == "balance" or rankings.lower() == "bal":
            value = "balance"
        with open("pastries.json", "r") as f:            
            users = json.load(f)
        count = 0
        user_list = ""
        sorted_users = sorted(list(users.items()), key = lambda kv: kv[1].get(value, 0), reverse = True)
        if value == "pastry_number" or value == "pastry": #Pastry leaderboard
            while count in range(0,lb_no):
                user_place = f"<@{sorted_users[count][0]}> - {list(sorted_users[count][1].items())[1][1]} pastries"
                user_list += user_place + "\n"
                count += 1
            await ctx.send(embed = discord.Embed(colour = 0xFFF8F6, title = "Pastry Leaderboard:", 
            description = f"Top {lb_no}:\n{user_list}"))
        elif value == "balance": #Money leaderboard
            await ctx.send(embed = discord.Embed(colour = 0xFFD700, title = "Money Leaderboard:", 
            description = f"Top 3:\n<@{sorted_users[0][0]}> - ${list(sorted_users[0][1].items())[5][1]}\n<@{sorted_users[1][0]}> - ${list(sorted_users[1][1].items())[5][1]}\n<@{sorted_users[2][0]}> - ${list(sorted_users[2][1].items())[5][1]}"))
            
        #Leaderboard per server

def setup(bot):
    bot.add_cog(Rankings(bot))