import argparse
import discord
import asyncio
import time
from lib import eventCallBacks

parser = argparse.ArgumentParser(description='User interface for Discord API Interaction')
parser.add_argument('--token', help='Token to use to connect bot to channels')

import discord
import asyncio

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = None



    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def testSleep(self):
        print('Staring test')
        await asyncio.sleep(1)
        print('finished test')

    async def my_background_task(self):
        await self.wait_until_ready()

        while not self.is_closed():
            usrInp = input(
                "\n\nYour options are: \n\tsend - send a message\n\tinfo - view current bot info\n\tdisonnect - disconnect this bot\n\n What would you like to do?:")

            if usrInp == "info":
                await self.printBotInfo()
                # await self.testSleep()
            elif usrInp == "send":
                channel = self.get_channel(1234567)  # channel ID goes here
                await channel.send("hi")
            elif usrInp == "disconnect":
                print("Disconnecting...")
            await asyncio.sleep(1) # task runs every 60 seconds

    async def printBotInfo(self):
        print("-----------BOT INFORMATION----------")
        print("Connection state: {}".format(self.is_ready()))
        print("Username: {}".format(self.user.name))
        print("User ID: {}".format(self.user.id))
        print("Connection state: {}".format(client.is_ready()))
        print("Guilds bot belongs to:")
        guilds = await client.fetch_guilds(limit=10).flatten()
        for guild in self.guilds:
            print("\t{}".format(guild))
            print("\tNumber of members: {}".format(guild.member_count))
            print("\tNumber of channels: {}".format(len(guild.channels)))

if __name__ == '__main__':
    print("Starting")
    args = parser.parse_args()
    intents = discord.Intents(messages=True, guilds=True,members=True)
    client = MyClient(intents=intents)
    client.run(args.token)
