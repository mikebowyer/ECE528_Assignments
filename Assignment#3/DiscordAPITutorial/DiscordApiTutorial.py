import argparse
import discord
import asyncio
import time
import tkinter as tk
import threading
from lib import eventCallBacks
from functools import partial

parser = argparse.ArgumentParser(description='User interface for Discord API Interaction')
parser.add_argument('--token', help='Token to use to connect bot to channels')
args = None
client = discord.Client()

async def say_after(delay, what):
    # await asyncio.sleep(delay)
    print(what)

async def user_input():
    while True:
        usrInp = input("Enter your value: ")
        if usrInp == "connect":
            await say_after(1,"connect")
        elif usrInp == "send":
            await say_after(1, "send")
        elif usrInp == "user":
            await say_after(1, "user")
        else:
            print("Nothing")

async def main():
    print(f"started at {time.strftime('%X')}")

    asyncio.create_task(user_input())
    # await user_input(2, 'world')

    print(f"finished at {time.strftime('%X')}")



if __name__ == '__main__':
    print("Starting")
    args = parser.parse_args()
    asyncio.run(main())