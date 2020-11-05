import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv('.env')

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='.', intents=intents)


@client.command()
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def reload(context, extension):
    client.reload_extension(f'cogs.{extension}')


@client.command()
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('TOKEN'))
