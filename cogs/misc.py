import discord
from discord.ext import commands


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game('.help for commands'))
        print('Bot is ready.')

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        if isinstance(error, commands.CommandNotFound):
            await context.send('Invalid command.')

    @commands.command()
    async def ping(self, context):
        # await context.send('Pong!')
        await context.send(f'Pong! {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(Misc(client))
