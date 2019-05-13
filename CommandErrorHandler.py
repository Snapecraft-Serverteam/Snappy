import traceback
import sys
from discord.ext import commands
import discord
from Errors import PlayerNotFoundError
from mysql.connector.errors import InterfaceError, ProgrammingError


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""
        print("on_command_error")

        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'`{ctx.command}` ist deaktiviert!')

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(f'`{ctx.command}` kann nicht in DMs benutzt werden!')

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('Ein Argument fehlt. Gib `?help` ein, um eine Hilfe der Commands anzuzeigen.')

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send('Command nicht gefunden. Gib `?help` ein, um eine Liste aller Commands anzuzeigen.')

        elif isinstance(error, PlayerNotFoundError):
            return await ctx.send('Spieler nicht gefunden. Vergewissere dich noch einmal, ob der eingegebene Name korrekt ist.')

        elif isinstance(error, KeyError):
            return await ctx.send(
                'Spieler nicht gefunden. Vergewissere dich noch einmal, ob der eingegebene Name korrekt ist.')

        elif isinstance(error, InterfaceError):
            return await ctx.send('Konnte nicht mit MySQL Datenbank verbinden. Bitte wende dich an einen Admin / Developer.')

        elif isinstance(error, ProgrammingError):
            return await ctx.send('Konnte nicht mit MySQL Datenbank verbinden. Bitte wende dich an einen Admin / Developer.')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
