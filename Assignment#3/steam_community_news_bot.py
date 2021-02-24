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
                    returnMessage = self.addNewCommunityNews(message)
                elif "latest" in message.content:
                    url = self.getNewsURLForThisChannel(message.channel)
                    if url != None:
                        latestAnnouncment = newsParser.getLatestAccouncement(url)
                        returnMessage = latestAnnouncment["title"]
                    else:
                        returnMessage = "This channel is not associated with a Steam Community News URL! Add the " \
                                        + "community URL using the add option.\n" \
                                        + '\tadd <steam community news URL> - Causes any new news posted on the steam community news ' \
                                        + 'page to sent to this channel\n '
                else:
                    returnMessage = self.getHelpMessage()

        return returnMessage

    def getHelpMessage(self):
        helpMessage = "Thanks for tagging Steam Community Bot! \n" \
                      + "There are two simple commands to use this bot: add & latest. \n" \
                      + '\tadd <steam community news URL> - Causes any new news posted on the steam community news page to sent to this channel\n' \
                      + '\tlatest - Causes latest news on steam community to be sent to this channel'
        return helpMessage

    def getNewsURLForThisChannel(self, channel):
        returnURL = None
        for community in self.jsonData["Communities"]:
            if channel.name == community["channelName"]:
                print("match")
                returnURL = community["url"]
                break
        return returnURL

    def addNewCommunityNews(self, message):
        returnMessage = 'Default error message'

        if len(message.content.split()) >= 2:
            url = message.content.split()[2]
            # TODO: Check if it is a valid steam community link
            newJsonEntry = {"channelName": message.channel.id,
                            "channelId": message.channel.name,
                            "url": url,
                            "last_patch_title": ""
                            }
            self.jsonData['Communities'].append(newJsonEntry)
            self.writeJsonData()
            returnMessage = "Adding new community to this channel. Expect news from the steam community at {} to be posted to this channel!".format(
                url)
        else:
            returnMessage = 'Invalid URL Provided, please provide valid steam community news URL. EG: https://steamcommunity.com/app/892970/'

        return returnMessage

    def writeJsonData(self):
        with open(self.jsonConfigPath, 'w') as configFile:
            json.dump(self.jsonData, configFile)
