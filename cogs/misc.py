import email
import imaplib
import os
import quopri

import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv('../.env')
USER = os.getenv('EMAIL_USER')
PASSWORD = os.getenv('EMAIL_PASS')

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

    @commands.command(name='-.', help=".-.")
    async def emote1(self, context):
        await context.send('.-.')

    @commands.command(name='_.', help="._.")
    async def emote2(self, context):
        await context.send('._.')

    # def get_problem(self):
    #     mail = imaplib.IMAP4_SSL("imap.gmail.com")
    #
    #     mail.login(user=USER, password=PASSWORD)
    #     mail.select('"Daily Coding Problem"')
    #
    #     result, data = mail.uid('search', None, "ALL")
    #     msgs = data[0].split()
    #     most_recent = msgs[-1]
    #
    #     result, data = mail.uid('fetch', most_recent, '(RFC822)')
    #
    #     raw = data[0][1]
    #     decoded = quopri.decodestring(raw)
    #     emailMsg = email.message_from_bytes(decoded)
    #     payload = emailMsg.get_payload()
    #     sep = "printable"
    #     stripped = payload.split(sep, 1)[1]
    #     sep = "--------"
    #     stripped = stripped.split(sep, 1)[0]
    #
    #     problem = stripped.strip()
    #     return problem
    #
    # @commands.command(name='problem', help="To get the latest Daily Coding Problem")
    # async def problem(self, context):
    #     temp = self.get_problem()
    #     ebd = discord.Embed(colour=discord.Colour.dark_teal())
    #     ebd.add_field(name='Problem: ', value=temp, inline=False)
    #     await context.message.channel.send(embed=ebd)

    def get_problem(self, num):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        mail.login(user=USER, password=PASSWORD)
        mail.select('"Daily Coding Problem"')

        result, data = mail.uid('search', None, "ALL")
        msgs = data[0].split()
        if num == -1:
            most_recent = msgs[num]
        elif num > len(msgs):
            return f"There are only {len(msgs)} Daily Coding Problems so far."
        else:
            most_recent = msgs[num-1]

        result, data = mail.uid('fetch', most_recent, '(RFC822)')

        raw = data[0][1]
        decoded = quopri.decodestring(raw)
        emailMsg = email.message_from_bytes(decoded)
        payload = emailMsg.get_payload()
        sep = "printable"
        stripped = payload.split(sep, 1)[1]
        sep = "--------"
        stripped = stripped.split(sep, 1)[0]

        problem = stripped.strip()
        return problem

    @commands.command(name='problem', help="To get a Daily Coding Problem.")
    async def problem(self, context, num=-1):
        temp = self.get_problem(num)

        ebd = discord.Embed(colour=discord.Colour.dark_teal())
        ebd.add_field(name='Problem: ', value=temp, inline=False)
        await context.message.channel.send(embed=ebd)


def setup(client):
    client.add_cog(Misc(client))
