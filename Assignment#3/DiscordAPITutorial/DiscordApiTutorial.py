

import argparse, asyncio, discord, sys, time
import tkinter as tk
from lib import eventCallBacks

parser = argparse.ArgumentParser(description='Bot to check for latest patches for a steam community news')
parser.add_argument('--token', help='Token to use to connect bot to channels')
parser.add_argument('--jsonConfig', help='JSON config file which contains which guilds')


mainWindow = tk.Tk()
mainWindow.title("Discord Bot Tutorial")
mainWindow.geometry("300x100")

#Button
sendMsgBtn = tk.Button(
    text="Send a message",
    command=eventCallBacks.sendMsgBtnClk,
)
getUserInfoBtn = tk.Button(
    text="Get user information",
    command=eventCallBacks.getUserInfoBtnClk,
)
connect = tk.Button(
    text="Connect bot to discord",

)
connect.pack()
sendMsgBtn.pack()
getUserInfoBtn.pack()

mainWindow.mainloop()

