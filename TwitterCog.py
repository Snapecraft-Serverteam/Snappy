import discord
from discord.ext import commands
from twython import Twython
from Data import TokenConfig, RolesConfig


class TwitterCog(commands.Cog):
    twitter = None

    def __init__(self, bot):
        self.bot = bot
        tokens = TokenConfig()
        cred = tokens.get_twitter_tokens()
        self.twitter = Twython(cred.get_apikey(),cred.get_apisecret(),cred.get_accesstoken(),cred.get_accesstokensecret())

    @commands.command()
    async def twitterit(self, obj, msg):
        roles = RolesConfig()
        twitterrole = roles.get_role("Twitter")
        if obj.guild is None:
            return
        if obj.guild.get_role(int(twitterrole)) is None:
            print("Role Twitter with id " + twitterrole + " not found")
            return
        if obj.guild.get_role(int(twitterrole)) not in obj.message.author.roles:
            await obj.channel.send('Du hast keine Rechte, das Twitterfeature zu nutzen.')
            return

        message = obj.message.content
        message = message.replace(self.bot.command_prefix + "twitterit ", "")

        print("[TWITTER] Sending....")
        print("[TWITTER] " + message + "\n\n Von " + obj.author.name + " aus dem Snapecraft-Serverteam")
        await self.sendtweet(message + "\n\n Von " + obj.author.name + " aus dem Snapecraft-Serverteam")
        print("[TWITTER] Gesendet.")

    async def sendtweet(self, msg):
        print()
        self.twitter.update_status(status=msg)
