import asyncio
import discord

from discord.ext import commands, tasks
from mojang_api import Player

from CommandErrorHandler import CommandErrorHandler
from Data import Database
from Data import OntimeConfig, VerifyConfig, CommonConfig, RolesConfig
from Data import Util
from Errors import PlayerNotFoundError

bot = commands.Bot(command_prefix='?')

bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged on as', bot.user)
    update_roles.start()
    await bot.change_presence(activity=discord.Game(name="?help"))


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Argumente mit <spitzen> Klammern sind verpflichtend, solche mit [eckigen] sind optional.", color=0x36df9a)
    embed.set_author(name="Snappy Commandhilfe")
    embed.add_field(name='?ontime <Spieler>',
                    value='Zeigt die "ingame" Online-Zeit des angegebenen Spielers an.',
                    inline=False)
    embed.add_field(name='?serverlist [Server]',
                    value='Zeigt, wenn kein Argument angegeben ist, die Spielerliste aller Server an. Andernfalls nur die des jeweiligen Servers.',
                    inline=False)
    embed.add_field(name='?verify', value = 'Gibt dir einen Command, den du ingame eingeben kannst, um dich auf diesem Discord Server zu verifizieren.', inline=False)
    embed.add_field(name='?uuid <Spieler>', value='Zeigt die UUID zum angegebenen Spieler an.', inline=True)
    embed.add_field(name='?help', value='Zeigt diese Hilfe an.', inline=True)
    embed.set_footer(icon_url="https://cdn.discordapp.com/icons/475787745801797633/3d144f5b28024105289216e5dc2151a4.png?", text="https://snapecraft.net")
    await ctx.send(embed=embed)


@bot.command()
async def verify(ctx, name):
    code = Util().id_generator(5)

    if not Player(username=name):
        raise PlayerNotFoundError

    db = Database(host=VerifyConfig().get_host(), user=VerifyConfig().get_user(), database=VerifyConfig().get_db(), passwd=VerifyConfig().get_passwd())
    temp_verification = db.create_temp_verfication(id=str(ctx.author.id), code=code, uuid=Player(username=name).uuid)

    if temp_verification == 0:
        await ctx.send("Gib zum Verifizieren folgenden Command auf einem der Server ein:\n`/verify " + code + "`\nHinweis: Es kann bis zu " + str((int(CommonConfig().get_update_interval())/60)) + " Minuten dauern, bis du deinen Rang erhälst!")
    elif temp_verification == 1:
        await ctx.send("Account bereits verifiziert!")

    elif temp_verification == 2:
        new_code = Util().id_generator(5)
        db.delete_code(str(ctx.author.id), Player(username=name).uuid)
        db.create_temp_verfication(str(ctx.author.id), Player(username=name).uuid, new_code)
        await ctx.send("Command wurde bereits eingegeben, deshalb musste ein neuer Command generiert werden:\n`/verify " + new_code + "`")


@bot.command()
async def ontime(ctx, name):
    for x in OntimeConfig().get_tables():
        await ctx.send(x + ":  " + Util().formatDate(Database(host=OntimeConfig().get_host(), user=OntimeConfig().get_user(), database=OntimeConfig().get_db(), passwd=OntimeConfig().get_passwd()).get_ontime(name, x)))


@bot.command()
async def uuid(ctx, name):
    await ctx.send("UUID von " + name + ": " + Player(username=name).uuid)


@bot.command()
async def serverlist(ctx):
    await ctx.send("coming soon(TM)")


@tasks.loop(seconds=int(CommonConfig().get_update_interval()))
async def update_roles():
    guild = bot.get_guild(int(CommonConfig().get_guild_id()))
    roles = RolesConfig().get_roles()
    mc_players = Database(host=VerifyConfig().get_host(), user=VerifyConfig().get_user(), database=VerifyConfig().get_db(), passwd=VerifyConfig().get_passwd()).get_data()

    for mc_player in mc_players:
        if guild.get_member(int(mc_player['discord'])) is not None:
            member = guild.get_member(int(mc_player['discord']))
            if mc_player['mcrole'].lower() in roles:
                role = guild.get_role(int(roles[mc_player['mcrole'].lower()]))
                if role not in member.roles:
                    print(member.name + "'s Rollen wurden geupdatet")
                    await member.add_roles(role)
                    await member.send("Deine Rollen wurden aktualisiert!")
            verified = guild.get_role(int(CommonConfig().get_verified_role()))
            if verified not in member.roles:
                print(member.name + " hat sich verifiziert")
                await member.add_roles(verified)
                await member.send("Du wurdest erfolgreich verifiziert!")
                await guild.get_channel(int(CommonConfig().get_general())).send(member.mention + " hat sich erfolgreich verifiziert!")
                await member.edit(nick=Player(uuid=mc_player['uuid']).username)


def setup(setup_bot):
    setup_bot.add_cog(CommandErrorHandler(setup_bot))
    setup_bot.run(open("token.txt").read())


setup(bot)
