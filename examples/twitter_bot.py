import json
import os

from dotenv import load_dotenv

from base_connectors.baseBot import BaseBot
from functionalities.twitter import send_tweet

load_dotenv()


class TwitterBot(BaseBot):
    def __init__(
        self,
        discord_token=os.getenv("DISCORD_TOKEN"),
        twitter_token=os.getenv("TWITTER_TOKEN"),
    ):
        super().__init__(discord_token=discord_token)
        if twitter_token is None:
            print("No twitter token provided")
        else:
            self.twitter_token = twitter_token
        self.guilds = {}

        @self.bot.event
        async def on_ready():
            self.update_guilds()
            print("Online and guilds info saved to self.guilds.")
            print(f"Bot is connected to {len(self.guilds)} discord servers")

        @self.bot.command(name="tweet")
        async def tweet(ctx, *args):
            try:
                send_tweet(
                    " ".join(args),
                    api_key=self.guilds[ctx.guild.id]["twitter_account"]["api_token"],
                    api_key_secret=self.guilds[ctx.guild.id]["twitter_account"][
                        "api_secret"
                    ],
                )
                await ctx.send("Tweeted")
            except KeyError:
                await ctx.send(
                    "No twitter account linked to this server Try !link_twitter"
                )
            except Exception as e:
                await ctx.send(f"Error: {e}")

        @self.bot.command(name="link_twitter")
        async def link_twitter(ctx, *args):
            self.guilds[ctx.guild.id]["twitter_account"] = {}
            self.guilds[ctx.guild.id]["twitter_account"]["name"] = args[0]
            self.guilds[ctx.guild.id]["twitter_account"]["api_token"] = args[1]
            self.guilds[ctx.guild.id]["twitter_account"]["api_secret"] = args[2]
            with open("guilds.json", "w") as f:
                json.dump(self.guilds, f, indent=4)

    def start(self):
        print("Twitter Bot Started")
        self.bot.run(self.discord_token)

    def update_guilds(self):
        print("Updating guilds")
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
        with open("guilds.json", "w+") as f:
            json.dump(self.guilds, f, indent=4)


TwitterBot().start()
