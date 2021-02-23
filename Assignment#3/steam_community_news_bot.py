import discord
from discord.ext import commands
import json
from lib import steam_community_news_parser as newsParser


class GuildChannelSteamNews:
    def __init__(self, guild, channel, steamNewsURL):
        self.guild = guild
        self.channel = channel
        self.steamsNewsURL = steamNewsURL


class SteamCommunityNewsBot:
    def __init__(self):
        self.jsonConfigPath = None
        self.jsonData = None
        self.bot = commands.Bot(command_prefix='!')

    def readConfig(self, jsonConfigPath):
        try:
            f = open(jsonConfigPath, )
            self.jsonConfigPath = jsonConfigPath
            self.jsonData = json.load(f)
            return True
        except:
            return False

    def handleIncomingMessage(self, message):
        returnMessage = None
        for mention in message.mentions:
            if mention.id == self.bot.user.id:
                if "add" in message.content:
                    returnMessage = "Adding new steam community news to this channel"
                    returnMessage = self.addNewCommunityNews(message)
                elif "latest" in message.content:
                    returnMessage = "grabbing latest content for this game"
                    url = self.getNewsURL(message.channel)
                    latestAnnouncment = newsParser.getLatestAccouncement(url)
                    returnMessage = latestAnnouncment["title"]
                else:
                    returnMessage = self.getHelpMessage()

        return returnMessage

    def getHelpMessage(self):
        helpMessage = "Thanks for tagging Steam Community Bot! \n" \
                      + "There are two simple commands to use this bot: add & latest. \n" \
                      + '\tadd <steam community news URL> - Causes any new news posted on the steam community news page to sent to this channel\n' \
                      + '\tlatest - Causes latest news on steam community to be sent to this channel'
        return helpMessage

    def getNewsURL(self, channel):
        returnURL = None
        for community in self.jsonData["Communities"]:
            if channel.name == community["channel"]:
                print("match")
                returnURL = community["url"]
                break
        return returnURL

    def addNewCommunityNews(self, message):
        returnMessage = 'Default error message'
        channelID = message.channel.id
        channelName = message.channel.name
        if len(message.content.split()) >= 2:
            url = message.content.split()[2]
            #TODO: Check if it is a valid steam community link
            returnMessage = "Adding new community to this channel. Expect news from the steam community at {} to be posted to this channel!".format(url)
        else:
            returnMessage = 'Invalid URL Provided, please provide valid steam community news URL. EG: https://steamcommunity.com/app/892970/'

        return returnMessage
