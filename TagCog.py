import asyncio

import discord
from discord.ext import commands
from fuzzywuzzy import process

from Data import TagConfig, RolesConfig


class TagCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, *args):
        query = ''
        for arg in args:
            query = query + ' ' + arg

        # trimming the whitespace at the start and end of the arg string
        query = query.lstrip().rstrip()

        if not query.startswith("create") and not query.startswith("delete") and not query.startswith("list"):
            async with ctx.channel.typing():
                str2Match = query
                strOptions = TagConfig().get_all_tags()

                # Getting a list of tuples that includes the tag name and the match percentage
                highest = process.extract(str2Match, strOptions)

                # Finding the three best matches and sorting them
                threeBest = sorted(highest, reverse=True, key=lambda x: x[1])[:3]

                if threeBest[0][1] > 80:
                    match = threeBest[0]
                    await self.send_formatted_tag(str(match[0]), TagConfig().get_tag(TagConfig().get_path_of_tag(str(match[0]))), ctx.channel)
                else:
                    await ctx.send("Nicht sicher, was du gemeint hast. Ist dein Tag hier dabei?\n\n`" + str(threeBest[0][0]) + "`  (" + str(threeBest[0][1]) + "%)\n`" + str(threeBest[1][0]) + "`  (" + str(threeBest[1][1]) + "%) \n`" + str(threeBest[2][0]) + "`  (" + str(threeBest[2][1]) + "%)")
        else:
            member = ctx.message.author
            # Check if member has a higher role than 'Moderator'
            # if member.top_role > ctx.guild.get_role(int(RolesConfig().get_roles()['Moderator'])):
            if 0 == 0: # (<===) TODO: Change dis
                if query.startswith("create"):
                    def check(m):
                        return m.author == ctx.author
                    await ctx.channel.send("Erstelle Tag '" + query.split(' ')[1] + "'. Bitte gib den Text in __einer Nachricht__ an!")

                    try:
                        text = await self.bot.wait_for('message', check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.channel.send("Breche ab, Timeout erreicht!")
                    else:
                        self.create_tag(query.split(' ')[1:], text.content, ctx.message.author.name)
                        await ctx.channel.send("Tag erstellt!")
                    # print(query)

                elif query.startswith("delete"):
                    pass
                elif query.startswith("list"):
                    await ctx.channel.send("Folgende Tags sind verfügbar:\n\n" + '\n'.join(TagConfig().get_all_tags()))
            else:
                await ctx.send("Du hast leider nicht die nötige Berechtigung, um diesen Command auszuführen.")

    async def send_formatted_tag(self, tag_name, tag_text: str, channel):
        if tag_text.startswith('@'):
            author = tag_text.split('\n')[0][1:]

            embed = discord.Embed()

            embed.add_field(name=tag_name, value="by " + author, inline=False)
            await channel.send(embed=embed)
            await channel.send('\n'.join(tag_text.split('\n')[1:]))
        else:
            author = "System"

            embed = discord.Embed()

            embed.add_field(name=tag_name, value="by " + author, inline=False)
            await channel.send(embed=embed)
            await channel.send('\n'.join(tag_text.split('\n')[1:]))

    def create_tag(self, tag_name, tag_text, author):

        if isinstance(tag_name, list):
            tag_name = '_'.join(tag_name)

        file = open("tags/" + tag_name + ".txt", "w+")
        file.write("@" + author + "\n")
        file.write(tag_text)
        file.close()
        TagConfig().add_tag_to_config("tags/" + tag_name + ".txt", tag_name)
