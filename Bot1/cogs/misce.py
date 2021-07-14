import discord
from discord import Embed
from discord.ext import commands
import random

class Misce(commands.Cog):

    def __innit__(self, client):
        self.client = client
    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready, fitted with misce")

    #commands
    @commands.command()
    async def hi(self,ctx):
        greetings = ["Hello!",
                     "Greetings",
                     "G'day",
                     "Hi",
                     "你好",
                     "您好"]
        await ctx.send(f"{random.choice(greetings)}")

    def is_it_me(self, ctx):
        return ctx.author.id == 202707943223721984

    @commands.command()
    @commands.check(is_it_me)
    async def example(self, ctx):
        await ctx.send(f"Hi I'm {ctx.author}")

    @commands.command(aliases=["speak", "talk"])
    async def say(self, ctx, *, sentence):
        await ctx.send(f"{sentence}")

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question = ""):
        responses = ["Yes",
                     "Definitely",
                     "No Brainer",
                     "No",
                     "It is not in my position to answer that...",
                     "Unfortunately, yes",
                     "stfu",
                     "I don't know",
                     "Fuck no",
                     "Fucking clown, ofc not",
                     "当然！"]
        if "?" == question[-1]:
                                                        #0xHEXCODE not HEXCODE
            em = Embed(title = f"question: {question}", colour = 0x00FF7F)
            em.description = f"{random.choice(responses)}"
            await ctx.send(embed = em)
        else:
            embed = discord.Embed(title = "Not a question", description = "Try again", colour = 0xFF0000)
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Misce(client))
