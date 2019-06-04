import math

from discord.ext import commands
from mojang_api import Player

from Data import Database, VerifyConfig, Util, CommonConfig
from Errors import PlayerNotFoundError


class VerifyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(ctx, name):
        code = Util().id_generator(5)

        if not Player(username=name):
            raise PlayerNotFoundError

        db = Database(host=VerifyConfig().get_host(), user=VerifyConfig().get_user(), database=VerifyConfig().get_db(),
                      passwd=VerifyConfig().get_passwd())
        temp_verification = db.create_temp_verfication(id=str(ctx.author.id), code=code,
                                                       uuid=Player(username=name).uuid)

        if temp_verification == 0:
            await ctx.send(
                "Gib zum Verifizieren folgenden Command auf einem der Server ein:\n`/verify " + code + "`\nHinweis: Es kann bis zu " + str(
                    math.floor(int(
                        CommonConfig().get_update_interval()) / 60)) + " Minuten dauern, bis du deinen Rang erhälst!")
        elif temp_verification == 1:
            await ctx.send("Account bereits verifiziert!")

        elif temp_verification == 2:
            new_code = Util().id_generator(5)
            db.delete_code(str(ctx.author.id), Player(username=name).uuid)
            db.create_temp_verfication(str(ctx.author.id), Player(username=name).uuid, new_code)
            await ctx.send(
                "Command wurde bereits eingegeben, deshalb musste ein neuer Command generiert werden:\n`/verify " + new_code + "`")
