import discord
from discord.ext import commands
import random
import config

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    print('Bot is ready.')


# print when user enters or leaves server
# @client.event
# async def on_member_join(member):
#     print(f'{member} has joined a server.')
# @client.event
# async def on_member_remove(member):
#     print(f'{member} has left a server.')

# ping command
@client.command()
async def ping(context):
    await context.send(f'Pong! {round(client.latency * 1000)}ms')


# 8ball command
# @client.command(aliases=['8ball'])
# async def _8ball(context, *, question):
#     responses = ['It is certain.',
#                  'It is decidedly so.',
#                  'Without a doubt.',
#                  'Yes - definitely.',
#                  'You may rely on it.',
#                  'As I see it, yes.',
#                  'Most likely.',
#                  'Outlook good.',
#                  'Yes.',
#                  'Signs point to yes.',
#                  'Reply hazy, try again.',
#                  'Ask again later.',
#                  'Better not to tell you now.',
#                  'Cannot predict now.',
#                  'Concentrate and ask again.',
#                  "Don't count on it",
#                  'My reply is no.',
#                  'My sources say no.',
#                  'Outlook not so good.',
#                  'Very doubtful.']
#     await context.send(f'Question: {question}\n8 Ball says {random.choice(responses)}')


@client.command()
async def clear(context, amount=5):
    await context.channel.purge(limit=amount + 1)
    await context.send(f'Deleted last {amount} messages')


@client.command()
async def kick(context, member: discord.Member, *, reason='None.'):
    await member.kick(reason=reason)


@client.command()
async def ban(context, member: discord.Member, *, reason='None.'):
    await member.ban(reason=reason)


client.run(config.token)
