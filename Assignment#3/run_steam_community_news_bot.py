import argparse
import json
from steam_community_news_bot import SteamCommunityNewsBot

parser = argparse.ArgumentParser(description='Bot to check for latest patches for a steam community news')
parser.add_argument('--token', help='Token to use to connect bot to channels')
parser.add_argument('--jsonConfig', help='JSON config file which contains which guilds')


steamCommunityNewsBot = SteamCommunityNewsBot()
@steamCommunityNewsBot.bot.event
async def on_message(message):
    # do something with message
    print(message.content)

    if message.content == 'hello bottymcbotface':
        await message.channel.send('hello!')

if __name__ == '__main__':

    args = parser.parse_args()

    while True:
        try:
            steamCommunityNewsBot.bot.loop.run_until_complete(steamCommunityNewsBot.bot.start(args.token))
        except KeyboardInterrupt:
            steamCommunityNewsBot.bot.loop.run_until_complete(steamCommunityNewsBot.bot.logout())
        finally:
            steamCommunityNewsBot.bot.loop.close()
