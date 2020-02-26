import asyncio
import math

import discord

from discord.ext import commands, tasks
from mojang_api import Player

from BrainstormCog import BrainstormCog
from CommandErrorHandler import CommandErrorHandler
from CoreCog import CoreCog
from Data import Database, ModulesConfig
from Data import OntimeConfig, VerifyConfig, CommonConfig, RolesConfig, TokenConfig
from Data import Util
from Errors import PlayerNotFoundError
from TagCog import TagCog
from VerifyCog import VerifyCog
from TwitterCog import TwitterCog

bot = commands.Bot(command_prefix='?')

bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged on as', bot.user)
    update_roles.start()
    await bot.change_presence(activity=discord.Game(name="?help"))




@tasks.loop(seconds=int(CommonConfig().get_update_interval()))
async def update_roles():
    if not ModulesConfig().is_enabled("verify"):
        return
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

    if ModulesConfig().is_enabled("core"):
        setup_bot.add_cog(CoreCog(setup_bot))

    if ModulesConfig().is_enabled("verify"):
        setup_bot.add_cog(VerifyCog(setup_bot))

    if ModulesConfig().is_enabled("tags"):
        setup_bot.add_cog(TagCog(setup_bot))

    if ModulesConfig().is_enabled("twitter"):
        setup_bot.add_cog(TwitterCog(setup_bot))

    if ModulesConfig().is_enabled("brainstorm"):
        setup_bot.add_cog(BrainstormCog(setup_bot))

    setup_bot.run(TokenConfig().get_token())


setup(bot)
