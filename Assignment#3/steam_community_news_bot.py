import discord
from lib import ssb_patch_parser
from lib import discord_utils


class GuildChannelSteamNews:
    def __init__(self, guild, channel, steamNewsURL):
        self.guild = guild
        self.channel = channel
        self.steamsNewsURL = steamNewsURL


class SteamCommunityNewsBotClient(discord.Client):
    async def on_message(self, message):
        # do something with message
        print(message.content)

        if message.content == 'hello bottymcbotface':
            await message.channel.send('hello!')
