from discord.ext import commands
import random
import akinator as ak


class Games(commands.Cog):

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

    @commands.command(name='aki', alias='akinator', help='Akinator')
    async def aki(self, context):
        await context.send("Akinator is here to guess!")

        def check(message):
            return message.author == context.author and message.channel == context.channel and message.content.lower() in ["y", "n",
                                                                                                               "p", "b"]
        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                await context.send(q)
                await context.send("Your answer:(y/n/p/b)")
                msg = await self.client.wait_for("message", check=check)
                if msg.content.lower() == "b":
                    try:
                        q = aki.back()
                    except ak.CantGoBackAnyFurther:
                        await context.send(e)
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await context.send(e)
                        continue
            aki.win()
            await context.send(
                f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?(y/n)\n"
                f"{aki.first_guess['absolute_picture_path']}\n\t")
            correct = await self.client.wait_for("message", check=check)
            if correct.content.lower() == "y":
                await context.send("Yay\n")
            else:
                await context.send("Oof\n")
        except Exception as e:
            await context.send(e)


def setup(client):
    client.add_cog(Games(client))
