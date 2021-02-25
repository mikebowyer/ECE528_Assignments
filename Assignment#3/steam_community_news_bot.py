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
        returnMsgList = []
        returnmsg = None #Stores normal text responses to send
        embedmsg = None #Stores embedded annoucnment information
        for mention in message.mentions:
            if mention.id == self.bot.user.id:
                print("INFO: New message in channel {} tagged this bot, responding.".format(message.channel.name))
                if "add" in message.content:
                    returnmsg, communityName = self.addNewCommunityNews(message)
                    addedSuccessFailMsg = {'embed': False, 'contents': returnmsg}
                    if communityName != None:
                        print("Need to find newest patch and share it")
                        embedmsg = self.getLatestAnnouncmentForCommunity(communityName)
                        latestAnnoucnmentMsg = {'embed': True, 'contents': embedmsg}
                    returnMsgList.append(addedSuccessFailMsg)
                    returnMsgList.append(latestAnnoucnmentMsg)
                elif "latest" in message.content:
                    # strip out community name from message: @SteamCommunityBot latest <community name>
                    communityName = " ".join(message.content.split()[2:])  # make a single string single spaced

                    if "all" in communityName:
                        #TODO: get all updates
                        print("All")
                    else:
                        embedmsg = self.getLatestAnnouncmentForCommunity(communityName)
                        if embedmsg == None:
                            noCommunityText = "No steam community of name {} is associated with this channel! Cannot get latest announcement.".format(communityName)
                            noCommunityMsg = {'embed': False, 'contents': noCommunityText}
                            returnMsgList.append(noCommunityMsg)
                        else:
                            latestAnnouncmentMsg = {'embed': True, 'contents': embedmsg}
                            returnMsgList.append(latestAnnouncmentMsg)
                elif "list" in message.content:
                    listMsg = {'embed': False, 'contents': self.getAllCommunityNameURLsMsg(message.channel)}
                    returnMsgList.append(listMsg)
                elif "remove" in message.content:
                    #strip out community name from message: @SteamCommunityBot Remove <community name>
                    communityName = " ".join(message.content.split()[2:])
                    removalSuccess = self.removeCommunity(communityName)

                    if removalSuccess:
                        successMsg = {'embed': False, 'contents': "Successfully removed announcements for {} from this channel".format(communityName)}
                        returnMsgList.append(successMsg)
                    else:
                        failMsg = {'embed': False,
                                      'contents': "Failed to removed announcements for {}, that community is not associated with this channel".format(
                                          communityName)}
                        returnMsgList.append(failMsg)
                else:
                    helpMsg = {'embed': False,
                                  'contents': self.getHelpMessage()}
                    returnMsgList.append(helpMsg)
                break

        return returnMsgList

    def getHelpMessage(self):
        helpMessage = "Thanks for tagging Steam Community Bot! \n" \
                      + "There are a few simple commands to use this bot:\n" \
                      + '\tadd <steam community news URL> - Causes any new news posted on the steam community news page to sent to this channel\n' \
                      + '\tlist - Shows all steam communities associated with this channel.\n' \
                      + '\tlatest <steam_community_name> - Causes latest news on the specified steam community to be sent to this channel.\n' \
                      + '\tlatest all - Causes latest news on all steam communities associated with this channel to be sent to this channel.\n' \
                      + '\tremove <steam community news URL> - Removes the specified steam community from this channel. \n'
        return helpMessage

    def getNewsURLForThisChannel(self, channelName):
        returnURL = None
        for community in self.jsonData["Communities"]:
            if channelName == community["channelName"]:
                returnURL = community["url"]
                break
        return returnURL

    def setLatestAccouncementTitle(self, communityName, accountmentTitle):
        for community in self.jsonData["Communities"]:
            if communityName == community["communityName"]:
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
            latestAnnouncment = newsParser.getLatestAccouncement(community['url'])
            #If new announcment
            if latestAnnouncment['title'] != community['lastAnnouncementTitle']:
                embeddedMessageForAnnouncment = self.createEmbedObjectForAnnouncment(latestAnnouncment)
                self.setLatestAccouncementTitle(community["communityName"], latestAnnouncment['title'])
                announceChannelPair = {"embedMsg": embeddedMessageForAnnouncment, "channelId": community["channelId"]}
                newAnnoucementChannelPairs.append(announceChannelPair)
        return newAnnoucementChannelPairs

    def getLatestAnnouncmentForCommunity(self, communityName):
        embeddedMessageForAnnouncment = None
        for community in self.jsonData['Communities']:
            if community['communityName'] == communityName:
                latestAnnouncment = newsParser.getLatestAccouncement(community['url'])
                embeddedMessageForAnnouncment = self.createEmbedObjectForAnnouncment(latestAnnouncment)
                self.setLatestAccouncementTitle(community['communityName'], latestAnnouncment['title'])

        return embeddedMessageForAnnouncment

    def getAllCommunityNameURLsMsg(self, channel):
        community_found=False
        returnMsg = "List of steam communities associated with this channel:\n"
        for community in self.jsonData['Communities']:
            if community['channelId'] == channel.id:
                newStr = "\t{} - {}\n".format(community['communityName'], community['url'])
                returnMsg= returnMsg + newStr
                community_found = True

        if not community_found:
            returnMsg=self.getNoAssociatedCommunitiesErrorMsg()

        return returnMsg

    def getNoAssociatedCommunitiesErrorMsg(self):
        returnMsg = "This channel is not associated with a Steam Community News! You can add a " \
        + "community URL using the add option.\n" \
        + '\tadd <steam community news URL> - Causes any new news posted on the steam community news ' \
        + 'page to sent to this channel\n '
        return returnMsg

    def removeCommunity(self, communityName):
        removalSuccess=False
        for community in self.jsonData['Communities']:
            if communityName in community['communityName']:
                self.jsonData['Communities'].remove(community)
                self.writeJsonData()
                removalSuccess=True

        return removalSuccess