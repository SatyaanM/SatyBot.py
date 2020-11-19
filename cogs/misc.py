import discord
from discord.ext import commands
from problem import get_problem


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

    @commands.command(aliases=['latency'], name='ping', help='To test latency')
    async def ping(self, context):
        await context.send(f'{round(self.client.latency * 1000)}ms')

    @commands.command(name='problem', help="To get the latest Daily Coding Problem")
    async def problem(self, context):
        await context.send(problem.get_problem())


def setup(client):
    client.add_cog(Misc(client))
