import discord
from discord.ext import commands
import json
from lib import ssb_patch_parser
from lib import discord_utils


class GuildChannelSteamNews:
    def __init__(self, guild, channel, steamNewsURL):
        self.guild = guild
        self.channel = channel
        self.steamsNewsURL = steamNewsURL


class SteamCommunityNewsBot:
    def __init__(self):
        self.jsonConfigPath = None
        self.jsonConfigData = None
        self.bot = commands.Bot(command_prefix='!')

    def updateConfig(self, jsonConfigPath):
        self.jsonConfigPath = jsonConfigPath
        f = open(jsonConfigPath, )
        self.jsonConfigData = json.load(f)

    def handleIncomingMessage(self, message):
        returnMessage= None
        for mention in message.mentions:
            if mention.id == self.bot.user.id:
                returnMessage = "Don't you @ me boy!"
        return returnMessage
