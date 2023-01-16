import sys
from abc import abstractmethod

from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()


class BaseBot:
    def __init__(self, discord_token, command_prefix="!"):
        super().__init__()
        # Start bot with token
        self.bot = Bot(command_prefix=command_prefix, intents=Intents.all())
        if discord_token is None:
            sys.exit("No discord token provided")
        self.discord_token = discord_token

        # Good practice should add a self.bot.event for on_ready and on_error
        # Inside on_ready, call self.update_guilds()
        # Other commands can be added here inside the __init__ method is the only place
        # where you can add commands to the bot and have them work to add a command:
        # @self.bot.command(name="command_name")
        # async def command_name(ctx, *args):
        #     await ctx.send("Hello World")
        # Another way of adding commands is by wrapping them in a function and calling a bit messy

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update_guilds(self):
        pass
