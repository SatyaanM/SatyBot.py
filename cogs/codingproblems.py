import email
import imaplib
import os
import quopri
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
from selenium import webdriver
import random

# environmental variables
load_dotenv('../.env')
USER = os.getenv('EMAIL_USER')
PASSWORD = os.getenv('EMAIL_PASS')
GOOGLE_CHROME_PATH = os.getenv('GOOGLE_CHROME_PATH')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

# chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_PATH
driver = webdriver.Chrome(chrome_options=chrome_options)

# local
# driver = webdriver.Chrome("C:/chromedriver_win32/chromedriver")


class CodingProblem(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        if isinstance(error, commands.CommandNotFound):
            await context.send('Invalid command.')

    @staticmethod
    def get_problem(num):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        mail.login(user=USER, password=PASSWORD)
        mail.select('"Daily Coding Problem"')

        # noinspection PyTypeChecker
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
        email_msg = email.message_from_bytes(decoded)
        payload = email_msg.get_payload()
        sep = "<title>"
        stripped = payload.split(sep, 1)[1]
        sep = "</title>"
        stripped = stripped.split(sep, 1)[0]
        subject = stripped.strip()

        payload = email_msg.get_payload()
        sep = "printable"
        stripped = payload.split(sep, 1)[1]
        sep = "--------"
        stripped = stripped.split(sep, 1)[0]

        problem = stripped.strip()
        return [subject, problem]

    @commands.command(name='problem', help="To get a Daily Coding Problem.")
    async def problem(self, context, num=-1):
        problem = self.get_problem(num)

        ebd = discord.Embed(colour=discord.Colour.dark_teal())
        ebd.add_field(name=f'{problem[0]}', value=problem[1], inline=False)
        await context.message.channel.send(embed=ebd)

    @staticmethod
    def screenshot(num):
        url = f'https://projecteuler.net/problem={num}'
        driver.set_window_size(720, 1280)
        driver.get(url)
        driver.save_screenshot("./problem.png")

    @commands.command(name='euler', help="To get a problem from Project Euler")
    async def euler(self, context):
        random.seed(time.time())
        num = random.randint(1, 751)
        self.screenshot(num)
        time.sleep(3)
        await context.send(file=discord.File('./problem.png'))


def setup(client):
    client.add_cog(CodingProblem(client))
