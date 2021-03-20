from discord.ext import commands
import random


class Magic8ball(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='8ball', help='Ask the magic 8 ball for guidance')
    async def _8ball(self, context, *, question):
        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes - definitely.',
                     'You may rely on it.',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good.',
                     'Yes.',
                     'Signs point to yes.',
                     'Reply hazy, try again.',
                     'Ask again later.',
                     'Better not to tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     "Don't count on it",
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        await context.send(f'Question: {question}\n8 Ball says {random.choice(responses)}')


def setup(client):
    client.add_cog(Magic8ball(client))
