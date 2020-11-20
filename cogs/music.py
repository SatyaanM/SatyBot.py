import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, context):
        self.client.voice = get(self.client.voice_clients, guild=context.guild)


def setup(client):
    client.add_cog(Music(client))
