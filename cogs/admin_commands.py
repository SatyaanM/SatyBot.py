import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, context, amount: int):
        await context.channel.purge(limit=amount+1)
        await context.send(f'Deleted last {amount} messages')

    @clear.error
    async def clear_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send('Please specify the amount of messages to delete.')
        if isinstance(error, commands.MissingPermissions):
            await context.send('You do not have permission to Manage Messages')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason='None.'):
        await member.kick(reason=reason)
        await context.send(f'Kicked {member.name}#{member.discriminator}')

    @kick.error
    async def kick_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send('Please specify the user to kick.')
        if isinstance(error, commands.MissingPermissions):
            await context.send('You do not have permission to Kick Users.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason='None.'):
        await member.ban(reason=reason)
        await context.send(f'Banned {member.name}#{member.discriminator}')

    @ban.error
    async def ban_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send('Please specify the user to ban.')
        if isinstance(error, commands.MissingPermissions):
            await context.send('You do not have permission to Ban Users.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, context, *, member):
        banned_users = await context.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member.name, member.discriminator):
                await context.guild.unban(user)
                await context.send(f'Unbanned {user.name}#{user.discriminator}')
                return

    @unban.error
    async def unban_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send('Please specify the user to unban.')
        if isinstance(error, commands.MissingPermissions):
            await context.send('You do not have permission to Unban Users.')


def setup(client):
    client.add_cog(AdminCommands(client))
