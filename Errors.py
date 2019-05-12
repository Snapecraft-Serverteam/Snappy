from discord.ext.commands.errors import CommandError


class PlayerNotFoundError(CommandError):
    pass


class PlayerFoundButNoDataError(CommandError):
    pass
