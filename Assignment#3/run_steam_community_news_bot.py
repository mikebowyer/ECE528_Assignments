import argparse
import json
from steam_community_news_bot import SteamCommunityNewsBotClient

parser = argparse.ArgumentParser(description='Bot to check for latest patches for a steam community news')
parser.add_argument('--token', help='Token to use to connect bot to channels')
parser.add_argument('--jsonConfig', help='JSON config file which contains which guilds')

if __name__ == '__main__':

    args = parser.parse_args()

    bot = SteamCommunityNewsBotClient()#args.jsonConfig)
    bot.run(args.token)
