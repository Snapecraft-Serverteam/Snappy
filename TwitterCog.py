import discord
from discord.ext import commands
from twython import Twython
from Data import TwitterLoginInfos, TokenConfig


class TwitterCog(commands.Cog):
    twitter = None

    def __init__(self, bot):
        self.bot = bot
        tokens = TokenConfig()
        cred = tokens.get_twitter_tokens()
        self.twitter = Twython(cred.get_apikey(),cred.get_apisecret(),cred.get_accesstoken(),cred.get_accesstokensecret())


    @commands.command()
    async def twitterit(self, obj, msg):
        message = obj.message.content
        message = message.replace(self.bot.command_prefix + "twitterit ", "")

        print("[TWITTER] Sending....")
        print("[TWITTER] " + message + "\n\n Von " + obj.author.name + " aus dem Snapecraft-Serverteam")
        await self.sendtweet(message + "\n\n Von " + obj.author.name + " aus dem Snapecraft-Serverteam")
        print("[TWITTER] Gesendet.")

    async def sendtweet(self, msg):
        print()
        self.twitter.update_status(status=msg)
