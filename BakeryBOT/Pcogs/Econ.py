import discord, random, json, Pchecks
from discord import Embed
from discord.ext import commands

pastry = "pastries.json"

class Econ(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Econ is ready")

    @commands.command(aliases = ['balance'])
    async def bal(self, ctx, member : discord.Member = None):
        with open(pastry, "r") as f:
            users = json.load(f)
        if member == None:
            member = ctx.author
        user = str(member.id)
        Pchecks.checks(users, user)
        await ctx.send(embed = discord.Embed(description = f"{member.mention}, has ${users[user]['balance']}", colour = 0x85bb65))

    @commands.command()
    @commands.cooldown(1, 2.5, commands.BucketType.user)
    async def sell(self, ctx, amount):
        with open(pastry, "r") as f:
            users = json.load(f)
        user = str(ctx.author.id)
        if users[user]["pastry_number"] <= 0:
            await ctx.send("You can't sell that many pastries...")
        else:
            users[user]["pastry_number"] -= amount
            profit = random.randint(1, amount)
            users[user]["balance"] += profit
            await ctx.send(embed = discord.Embed(description = f"You have sold {amount} pastries and earned {profit}! Keep baking!"))

    @commands.command()
    @commands.cooldown(1, 5, type = commands.BucketType.user)
    async def bet(self, ctx, bet_type, amount):
        with open(pastry, "r") as f:
            users = json.load(f)
        user = str(ctx.author.id)
        Pchecks.checks(users, user)
        
        if amount.lower() == "all":
            amount = int(users[user]["balance"])

        if users[user]["balance"] < int(amount):
            return await ctx.send("You don't have enough, go bake some more pastries")

        if int(amount) <= 0:
            return await ctx.send("You can't bet negative/nothing...")   

        if bet_type == None:
            bet_type = "coinflip"

        if bet_type == "coinflip":
            coinf = ["heads", "tails"]
            await ctx.send("Heads or Tails?")
            def check(message):
                return message.author == ctx.author

            coin_ht = await self.bot.wait_for("message", check=check, timeout=30.0)
            coin_r = random.choice(coinf)
            while coin_ht.content.lower() not in coinf:
                await ctx.send("What? Please bet\nHeads or Tails?")
                # rerun the check                
                coin_ht = await self.bot.wait_for("message", check=check, timeout=30.0)

            if coin_ht.content.lower() == coin_r:
                with open(pastry, "w") as f:
                    users[user]["balance"] += int(amount)
                    f.write(json.dumps(users, indent = 5))
                return await ctx.send(embed = discord.Embed(title = f"{coin_r.capitalize()}", description = f"You won ${int(amount)}!"))
            
            else:
                with open(pastry, "w") as f:
                    users[user]["balance"] -= int(amount)
                    users["202707943223721984"]["balance"] += int(amount)
                    f.write(json.dumps(users, indent = 5))
                return await ctx.send(embed = discord.Embed(title = f"{coin_r.capitalize()}", description = f"You lost ${int(amount)}!"))

    @commands.command()
    @commands.cooldown(1, 5, type = commands.BucketType.user)
    async def donate(self, ctx, member : discord.Member, amount : int):
        user = str(ctx.author.id)
        receiver = str(member.id)
        with open(pastry, "r") as f:
            users = json.load(f)
        Pchecks.checks(users, user)
        Pchecks.checks(users, receiver)
        if amount < 0:
            return await ctx.send("You can't give negative amounts")
        Pchecks.checks(users, user)
        if users[user]["balance"] < amount:
            return await ctx.send("You can't afford to donate that much")
        else:
            users[user]["balance"] -= amount
            users[receiver]["balance"] += amount
        with open(pastry, "w") as f:
            f.write(json.dumps(users, indent=5))
        await ctx.send(f"{ctx.author.mention} has given {member.mention} ${amount}")

def setup(bot):
    bot.add_cog(Econ(bot))