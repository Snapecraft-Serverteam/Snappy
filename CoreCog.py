import discord
from discord.ext import commands
from mojang_api import Player

from Data import OntimeConfig, Util, Database


class CoreCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ontime(self, ctx, name):
        for x in OntimeConfig().get_tables():
            await ctx.send(x + ":  " + Util().formatDate(Database(host=OntimeConfig().get_host(), user=OntimeConfig().get_user(), database=OntimeConfig().get_db(), passwd=OntimeConfig().get_passwd()).get_ontime(Player(username=name).uuid, x)))


    @commands.command()
    async def uuid(self, ctx, name):
        await ctx.send("UUID von " + name + ": " + Player(username=name).uuid)


    @commands.command()
    async def serverlist(self, ctx):
        await ctx.send("coming soon(TM)")

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Argumente mit <spitzen> Klammern sind verpflichtend, solche mit [eckigen] sind optional.",
            color=0x36df9a)
        embed.set_author(name="Snappy Commandhilfe")
        embed.add_field(name='?ontime <Spieler>',
                        value='Zeigt die "ingame" Online-Zeit des angegebenen Spielers an.',
                        inline=False)
        embed.add_field(name='?serverlist [Server]',
                        value='Zeigt, wenn kein Argument angegeben ist, die Spielerliste aller Server an. Andernfalls nur die des jeweiligen Servers.',
                        inline=False)
        embed.add_field(name='?verify <Spieler>',
                        value='Gibt dir einen Command, den du ingame eingeben kannst, um dich auf diesem Discord Server zu verifizieren.',
                        inline=False)
        embed.add_field(name='?uuid <Spieler>', value='Zeigt die UUID zum angegebenen Spieler an.', inline=True)
        embed.add_field(name='?help', value='Zeigt diese Hilfe an.', inline=True)
        embed.set_footer(
            icon_url="https://cdn.discordapp.com/icons/475787745801797633/3d144f5b28024105289216e5dc2151a4.png?",
            text="https://snapecraft.net")
        await ctx.send(embed=embed)

