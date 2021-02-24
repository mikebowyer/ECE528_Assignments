import argparse, asyncio, discord, sys
from steam_community_news_bot import SteamCommunityNewsBot

parser = argparse.ArgumentParser(description='Bot to check for latest patches for a steam community news')
parser.add_argument('--token', help='Token to use to connect bot to channels')
parser.add_argument('--jsonConfig', help='JSON config file which contains which guilds')

steamCommunityNewsBot = SteamCommunityNewsBot()


@steamCommunityNewsBot.bot.event
async def on_message(message):
    embedVar, returnMsg = steamCommunityNewsBot.handleIncomingMessage(message)
    if embedVar != None:
        await message.channel.send(embed=embedVar)
    elif returnMsg != None:
        await message.channel.send(returnMsg)


@steamCommunityNewsBot.bot.event
async def on_ready():
    print('Logged in as')
    print(steamCommunityNewsBot.bot.user.name)
    print(steamCommunityNewsBot.bot.user.id)
    print('------')


async def send_new_announcments():
    """
	Checks if a patch has been released for all games in patchbot.game_list.
	Every 5 minutes, all games update their patch information and games with new
	patches have their embed patch message pushed to their subscribed channels.
	"""
    await steamCommunityNewsBot.bot.wait_until_ready()
    while True:
        print("Checking for new announcements")
        await asyncio.sleep(300)
        newAnnouncementChannelPairs = steamCommunityNewsBot.getNewAnnouncementChannelPairs()
        print("\nChecking for new announcements\n")
        for announceChanPair in newAnnouncementChannelPairs:
            try:
                channel = steamCommunityNewsBot.bot.get_channel(announceChanPair['channelId'])
                await channel.send(embed=announceChanPair['embedMsg'])
            except (discord.DiscordException, discord.ClientException, discord.HTTPException, discord.NotFound):
                print("Could not connect to Discord when sending new annoucnement to channelID" + announceChanPair['channelId'])


if __name__ == '__main__':

    args = parser.parse_args()

    while True:
        try:
            if steamCommunityNewsBot.readConfig(args.jsonConfig):
                send_new_announcments_task = asyncio.ensure_future(send_new_announcments())
                steamCommunityNewsBot.bot.loop.run_until_complete(steamCommunityNewsBot.bot.start(args.token))
            else:
                print("Error reading config file, exiting.")
                break
        except KeyboardInterrupt:
            print("Keyboard interrupt detected, exiting.")
            steamCommunityNewsBot.bot.loop.run_until_complete(steamCommunityNewsBot.bot.logout())
            send_new_announcments_task.cancel()
            sys.exit(1)
        except:
            print("Something went wrong")
        finally:
            steamCommunityNewsBot.bot.loop.close()
