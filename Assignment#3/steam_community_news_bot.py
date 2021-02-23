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

    def readConfig(self, jsonConfigPath):
        try:
            f = open(jsonConfigPath, )
            self.jsonConfigPath = jsonConfigPath
            self.jsonConfigData = json.load(f)
            return True
        except:
            return False

    def handleIncomingMessage(self, message):
        returnMessage = None
        for mention in message.mentions:
            if mention.id == self.bot.user.id:
                if "add" in message.content:
                    returnMessage = "Adding new steam community news to this channel"
                elif "latest" in message.content:
                    returnMessage = "grabbing latest content for this game"
                else:
                    returnMessage = self.getHelpMessage()
        return returnMessage

    def getHelpMessage(self):
        helpMessage = "Thanks for tagging Steam Community Bot! \n" \
            + "There are two simple commands to use this bot: add & latest. \n" \
            + '\tadd <steam community news URL> - Causes any new news posted on the steam community news page to sent to this channel\n'\
            + '\tlatest - Causes latest news on steam community to be sent to this channel'
        return helpMessage
