import discord
import argparse
import asyncio
from lib import ssb_patch_parser
from lib import discord_utils




parser = argparse.ArgumentParser(description='Bot to check for latest patch notes from Super Smash Bros')
parser.add_argument('--token', help='Token to use to connect bot to channels')

if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.members = True
    print("INFO: Parsing input arguments")
    args = parser.parse_args()

    bot = discord.Client(intents=intents)

    ssb_patch = ssb_patch_parser.SSB()

    discord_utils.grabLastBotMessageInChannel()
    print("Yo")


    @bot.event
    async def on_message(message):
        # do something with message
        print(message.content)

        if message.content == 'hello bottymcbotface':
            await message.channel.send('hello!')


    bot.run(args.token)
