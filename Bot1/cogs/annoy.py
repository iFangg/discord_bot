import discord
from discord.ext import commands

class Annoy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send("test")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 202976948950007810: #user's ID
            await message.channel.send(f"stfu {message.author.mention}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 387389500298362881: #user's ID
            await message.channel.send("""
            Now Playing: Who asked Ft: Nobody\n───────────⚪────── ◄◄⠀▐▐⠀►► 𝟸:𝟷𝟾 / 𝟹:𝟻𝟼⠀───○ 🔊
            """)
            await message.channel.send(
            embed = discord.Embed(title = "CHIMP").set_image(
                url = "https://cdn.discordapp.com/attachments/673814669282115586/716453891578789928/unknown.png"
            )
        )

    @commands.command()
    async def die(self, ctx):
        await ctx.send("No thanks, buddy")

    @commands.command()
    async def spam(self, ctx, command, times : int):
        for i in range(times):
            await ctx.invoke(command)

def setup(client):
    client.add_cog(Annoy(client))
