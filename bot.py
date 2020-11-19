import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv('.env')

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='.', intents=intents)


@client.command(name='load', help='To load a specific cog')
@commands.has_permissions(administrator=True)
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')
    await context.send(f'{extension} loaded.')


@load.error
async def load_error(context, error):
    if isinstance(error, commands.MissingPermissions):
        await context.send('You are not permitted to load cogs.')
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send('Cog not found.')


@client.command(name='reload', help='To reload a specific cog')
@commands.has_permissions(administrator=True)
async def reload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await context.send(f'{extension} reloaded.')


@reload.error
async def reload_error(context, error):
    if isinstance(error, commands.MissingPermissions):
        await context.send('You are not permitted to reload cogs.')
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send('Cog not found.')


@client.command(name='unload', help='To unload a specific cog')
@commands.has_permissions(administrator=True)
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    await context.send(f'{extension} unloaded.')


@unload.error
async def unload_error(context, error):
    if isinstance(error, commands.MissingPermissions):
        await context.send('You are not permitted to unload cogs.')
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send('Cog not found.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('TOKEN'))
