import discord
from discord import Embed
from discord.ext import commands

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        guild = ctx.message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()

    #class Subclass(discord.VoiceClient):
        #def __init__(self, *args, **kwargs):
            #super().__init__(*args, **kwargs)

    @commands.command()
    async def create_ytdl_player(self, url: str):
        vc = ctx.voice_client
        #source = await discord.FFmpegOpusAudio.from_probe("song.webm", method='fallback')
        #vc.play(source)
        player = await vc.create_ytdl_player(url)
        self.players[ctx.guild.id] = player
        player.start()

def setup(client):
    client.add_cog(Music(client))
