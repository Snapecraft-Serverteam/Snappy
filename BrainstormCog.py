from discord.ext import commands

from Data import CommonConfig


class BrainstormCog(commands.Cog):

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith("!brainstorm"):

            thumpsup = '\U0001F44D'
            thumpsdown = '\U0001F44E'
            warn = '\U000026A0'

            channel = message.channel.id
            data = CommonConfig()
            if channel == int(data.get_brainstorm_channel()):

                await message.add_reaction(thumpsup)
                await message.add_reaction(thumpsdown)
                await message.add_reaction(warn)
        else:
            thumpsup = '\U0001F44D'
            thumpsdown = '\U0001F44E'
            warn = '\U000026A0'
            role = message.author.top_role
            if role.name is "Inhaber" or role.name is "Admin" or role.name is "Developer":
                messages = await message.channel.history(limit=200).flatten()
                for mess in messages:
                    await mess.add_reaction(thumpsup)
                    await mess.add_reaction(thumpsdown)
                    await mess.add_reaction(warn)
            await message.delete()

