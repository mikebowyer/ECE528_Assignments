import discord
from discord.ext import commands
from lib import ssb_patch_parser
from lib import discord_utils


class GuildChannelSteamNews:
    def __init__(self, guild, channel, steamNewsURL):
        self.guild = guild
        self.channel = channel
        self.steamsNewsURL = steamNewsURL


class SteamCommunityNewsBot:
    def __init__(self):
        self.jsonConfigPath = ""
        self.bot = commands.Bot(command_prefix='!')
