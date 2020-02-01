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
    async def twitterit(self, bot, msg):
        print("Twitterit: " + msg + " from " + bot.author.name)
        print("Sending...")
        await self.sendtweet(msg + "\n " + bot.author.name)
        print("Tweet gesendet. Nachricht: " + msg + "\n " + bot.author.name)

    async def sendtweet(self, msg):
        self.twitter.update_status(status=msg)
