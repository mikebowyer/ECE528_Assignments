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
                "Your options are: \n\tsend - send a message\n\tinfo - view current bot info\n\tdisonnect - disconnect this bot\n\n What would you like to do?:")

            if usrInp == "info":
                await self.testSleep()
            elif usrInp == "send":
                channel = self.get_channel(1234567)  # channel ID goes here
                await channel.send("hi")
            elif usrInp == "disconnect":
                print("Disconnecting...")
            await asyncio.sleep(1) # task runs every 60 seconds

if __name__ == '__main__':
    print("Starting")
    args = parser.parse_args()
    client = MyClient()
    client.run(args.token)
