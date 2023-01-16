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
        self.token = discord_token

    @abstractmethod
    def start(self):
        pass
