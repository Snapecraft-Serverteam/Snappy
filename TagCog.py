from discord.ext import commands
from fuzzywuzzy import process

from Data import TagConfig


class TagCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, *args):
        query = ''
        for arg in args:
            query = query + arg

        async with ctx.channel.typing():
            str2Match = query
            strOptions = TagConfig().get_all_tags()

            # Getting a list of tuples that includes the tag name and the match percentage
            highest = process.extract(str2Match, strOptions)

            # Finding the three best matches and sorting them
            threeBest = sorted(highest, reverse=True, key=lambda x: x[1])[:3]


            if threeBest[0][1] > 80:
                match = threeBest[0]
                await ctx.send("You meant `" + str(match) + "`, right?")
            else:
                await ctx.send("Not sure what you meant. Was it `" + str(threeBest[0]) + "`?")



