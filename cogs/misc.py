import discord
from discord.ext import commands


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.command()
    async def ping(self, context):
        # await context.send('Pong!')
        await context.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def clear(self, context, amount=5):
        await context.channel.purge(limit=amount+1)
        await context.send(f'Deleted last {amount} messages')

    @commands.command()
    async def kick(self, context, member: discord.Member, *, reason='None.'):
        await member.kick(reason=reason)
        await context.send(f'Kicked {member.name}#{member.discriminator}')

    @commands.command()
    async def ban(self, context, member: discord.Member, *, reason='None.'):
        await member.ban(reason=reason)
        await context.send(f'Banned {member.name}#{member.discriminator}')

    @commands.command()
    async def unban(self, context, *, member):
        banned_users = await context.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member.name, member.discriminator):
                await context.guild.unban(user)
                await context.send(f'Unbanned {user.name}#{user.discriminator}')
                return


def setup(client):
    client.add_cog(Misc(client))
