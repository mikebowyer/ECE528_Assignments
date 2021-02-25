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
        returnmsg = None #Stores normal text responses to send
        embedmsg = None #Stores embedded annoucnment information
        for mention in message.mentions:
            if mention.id == self.bot.user.id:
                print("INFO: New message in channel {} tagged this bot, responding.".format(message.channel.name))
                if "add" in message.content:
                    returnmsg, communityName = self.addNewCommunityNews(message)
                    if communityName != None:
                        print("Need to find newest patch and share it")
                        embedmsg = self.getLatestAnnouncmentForCommunity(communityName)

                elif "latest" in message.content:

                    url = self.getNewsURLForThisChannel(message.channel.name)
                    if url != None:
                        latestAnnouncment = newsParser.getLatestAccouncement(url)
                        embedmsg = self.createEmbedObjectForAnnouncment(latestAnnouncment)
                        self.setLatestAccouncementTitle(message.channel, latestAnnouncment['title'])
                    else:
                        returnmsg = self.getNoAssociatedCommunitiesErrorMsg()
                elif "list" in message.content:
                    returnmsg=self.getAllCommunityNameURLsMsg(message.channel)
                    print("List")

                elif "remove" in message.content:
                    print("remove")
                else:
                    returnmsg = self.getHelpMessage()
                break

        return embedmsg, returnmsg

    def getHelpMessage(self):
        helpMessage = "Thanks for tagging Steam Community Bot! \n" \
                      + "There are two simple commands to use this bot: add & latest. \n" \
                      + '\tadd <steam community news URL> - Causes any new news posted on the steam community news page to sent to this channel\n' \
                      + '\tlatest - Causes latest news on steam community to be sent to this channel'
        return helpMessage

    def getNewsURLForThisChannel(self, channelName):
        returnURL = None
        for community in self.jsonData["Communities"]:
            if channelName == community["channelName"]:
                returnURL = community["url"]
                break
        return returnURL

    def setLatestAccouncementTitle(self, channel, accountmentTitle):
        for community in self.jsonData["Communities"]:
            if channel == community["channelName"]:
                community['lastAnnouncementTitle'] = accountmentTitle
                break
        self.writeJsonData()

    def addNewCommunityNews(self, message):
        returnMessage = 'Default error message'
        communityName = None
        if len(message.content.split()) >= 2:
            url = message.content.split()[2]
            retrievedCommunityName = newsParser.getCommunityName(url)
            if retrievedCommunityName != None:
                latestAnnoucnment = newsParser.getLatestAccouncement(url)
                newJsonEntry = {
                                "communityName": retrievedCommunityName,
                                "channelId": message.channel.id,
                                "channelName": message.channel.name,
                                "url": url,
                                "lastAnnouncementTitle": latestAnnoucnment['title']
                                }
                self.jsonData['Communities'].append(newJsonEntry)
                self.writeJsonData()
                returnMessage = "Adding new community to this channel. Expect news from the steam community at {} to be posted to this channel!".format(
                    url)
                communityName=retrievedCommunityName
            else:
                returnMessage = 'Invalid URL Provided, please provide valid steam community news URL. EG: https://steamcommunity.com/app/892970/'
        else:
            returnMessage = 'Invalid URL Provided, please provide valid steam community news URL. EG: https://steamcommunity.com/app/892970/'

        return returnMessage, communityName

    def writeJsonData(self):
        with open(self.jsonConfigPath, 'w') as configFile:
            json.dump(self.jsonData, configFile)

    def createEmbedObjectForAnnouncment(self, announcment):
        embedObj = discord.Embed(title=announcment['title'], description=announcment['info'], url=announcment['url'],
                                 color=0x00ff00)
        if announcment['img_url'] != None:
            embedObj.set_image(url=announcment['img_url'])
        # embedObj.add_field(name="Field1", value="hi", inline=False)
        # embedObj.add_field(name="Field2", value="hi2", inline=False)
        return embedObj

    def getNewAnnouncementChannelPairs(self):
        newAnnoucementChannelPairs = []
        for community in self.jsonData["Communities"]:
            url = self.getNewsURLForThisChannel(community["channelName"])
            latestAnnouncment = newsParser.getLatestAccouncement(url)
            #If new announcment
            if latestAnnouncment['title'] != community['lastAnnouncementTitle']:
                embeddedMessageForAnnouncment = self.createEmbedObjectForAnnouncment(latestAnnouncment)
                self.setLatestAccouncementTitle(community["channelName"], latestAnnouncment['title'])
                announceChannelPair = {"embedMsg": embeddedMessageForAnnouncment, "channelId": community["channelId"]}
                newAnnoucementChannelPairs.append(announceChannelPair)
        return newAnnoucementChannelPairs

    def getLatestAnnouncmentForCommunity(self, communityName):
        embeddedMessageForAnnouncment = None
        for community in self.jsonData['Communities']:
            if community['communityName'] == communityName:
                latestAnnouncment = newsParser.getLatestAccouncement(community['url'])
                embeddedMessageForAnnouncment = self.createEmbedObjectForAnnouncment(latestAnnouncment)
                # self.setLatestAccouncementTitle(message.channel, latestAnnouncment['title'])

        return embeddedMessageForAnnouncment

    def getAllCommunityNameURLsMsg(self, channel):
        community_found=False
        returnMsg = "List of steam communities associated with this channel:\n"
        for community in self.jsonData['Communities']:
            if community['channelId'] == channel.id:
                newStr = "\t{} - {}\n".format(community['communityName'], community['url'])
                returnMsg= returnMsg + newStr
                community_found = False

        if not community_found:
            returnMsg=self.getNoAssociatedCommunitiesErrorMsg()

        return returnMsg

    def getNoAssociatedCommunitiesErrorMsg(self):
        returnMsg = "This channel is not associated with a Steam Community News! You can add a " \
        + "community URL using the add option.\n" \
        + '\tadd <steam community news URL> - Causes any new news posted on the steam community news ' \
        + 'page to sent to this channel\n '
        return returnMsg