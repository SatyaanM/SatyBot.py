import requests
from discord.ext import commands


class Memes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='humor', alias='humour', help='For random programming meme')
    async def humor(self, context):
        response = requests.get('https://meme-api.herokuapp.com/gimme/ProgrammerHumor')
        response = response.json()
        await context.message.channel.send(response['url'])

    @commands.command(name='meme', help='For random meme')
    async def meme(self, context):
        response = requests.get('https://meme-api.herokuapp.com/gimme')
        response = response.json()
        await context.message.channel.send(response['url'])

    @commands.command(name='wholesome', help='For wholesome meme')
    async def wholesome(self, context):
        response = requests.get('https://meme-api.herokuapp.com/gimme/wholesomememes')
        response = response.json()
        await context.message.channel.send(response['url'])


def setup(client):
    client.add_cog(Memes(client))
