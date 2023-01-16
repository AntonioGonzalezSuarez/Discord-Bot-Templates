import os
from datetime import datetime

import discord

from base_connectors.baseBot import BaseBot


class CustomBot(BaseBot):
    def __init__(self, discord_token: str = os.getenv("DISCORD_TOKEN")):
        super().__init__(discord_token, command_prefix="/")
        self.guilds = {}
        self.bot.remove_command("help")

        # Here you will put the commands
        @self.bot.command(name="help")
        async def help(ctx):
            await ctx.send("Hello friend i am here to help you")
            await ctx.send(
                "Current available functionalities: \n" "- /help\n" "- /info"
            )

        @self.bot.command(name="channel_info")
        async def channel_info(ctx):
            await ctx.send(self.guilds[ctx.guild.id]["channels"][ctx.channel.id])

        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=discord.Game(name="Do /help"))
            self.update_guilds()
            print("Online and guilds info saved to self.guilds.")
            print(
                f"At {datetime.now()} bot is connected to {len(self.guilds)} discord servers"
            )

        @self.bot.event
        async def on_guild_join(guild):
            for channel in guild.channels:
                if channel.type.name == "text":
                    await self.bot.get_channel(channel.id).send(
                        "Hello my friends. I am a bot desiged by Toni Tonin. "
                        "To get more info write !help"
                    )
            self.update_guilds()
            print(
                f"At {datetime.now()} bot is connected to new server. Giving service to: {len(self.guilds)} discord "
                f"servers"
            )

        @self.bot.event
        async def on_guild_remove(guild):
            del self.guilds[guild.id]
            print(
                f"At {datetime.now()} bot is disconnected from {guild.name}. Giving service to: {len(self.guilds)}"
                f" discord servers"
            )

    def start(self):
        self.bot.run(self.token)

    def update_guilds(self):
        for guild in self.bot.guilds:
            if str(guild.id) in self.guilds.keys():
                continue
            self.guilds[guild.id] = {}
            self.guilds[guild.id]["guild_name"] = guild.name
            self.guilds[guild.id]["channels"] = {}
            for channel in guild.channels:
                if channel.type.name != "category":
                    self.guilds[guild.id]["channels"][channel.id] = {}
                    self.guilds[guild.id]["channels"][channel.id][
                        "channel_name"
                    ] = channel.name
                    self.guilds[guild.id]["channels"][channel.id][
                        "channel_type"
                    ] = channel.type.name


bot = CustomBot()
bot.start()
