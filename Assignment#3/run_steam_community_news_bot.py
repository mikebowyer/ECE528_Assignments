import argparse
import json
from steam_community_news_bot import SteamCommunityNewsBot

parser = argparse.ArgumentParser(description='Bot to check for latest patches for a steam community news')
parser.add_argument('--token', help='Token to use to connect bot to channels')
parser.add_argument('--jsonConfig', help='JSON config file which contains which guilds')


steamCommunityNewsBot = SteamCommunityNewsBot()
@steamCommunityNewsBot.bot.event
async def on_message(message):
    returnMsg = steamCommunityNewsBot.handleIncomingMessage(message)
    if returnMsg != None:
        await message.channel.send(returnMsg)

@steamCommunityNewsBot.bot.event
async def on_ready():
    print('Logged in as')
    print(steamCommunityNewsBot.bot.user.name)
    print(steamCommunityNewsBot.bot.user.id)
    print('------')

if __name__ == '__main__':

    args = parser.parse_args()

    while True:
        try:
            if steamCommunityNewsBot.readConfig(args.jsonConfig):
                steamCommunityNewsBot.bot.loop.run_until_complete(steamCommunityNewsBot.bot.start(args.token))
            else:
                print("Error reading config file, exiting.")
                break
        except KeyboardInterrupt:
            steamCommunityNewsBot.bot.loop.run_until_complete(steamCommunityNewsBot.bot.logout())
        finally:
            steamCommunityNewsBot.bot.loop.close()
