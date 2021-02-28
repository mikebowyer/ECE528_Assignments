import tkinter as tk
import asyncio

async def sendMsgBtnClk(bot):
    print("send msessage button clicked")
    text_channel_list = []
    for server in bot.guilds:
        for channel in server.channels:
            if channel.type == 'Text':
                text_channel_list.append(channel)
    sendMsgWndw = tk.Tk()
    sendMsgWndw.title("Send Discord Message")
    sendMsgWndw.mainloop()

def getUserInfoBtnClk():
    print("get user information button clicked")
    getUserInfoWndw = tk.Tk()
    getUserInfoWndw.title("Current User Information")
    getUserInfoWndw.mainloop()

def showRcvdMsg():
    print("Got new message")
    getUserInfoWndw = tk.Tk()
    getUserInfoWndw.title("Recieved message")
    getUserInfoWndw.mainloop()

async def connectBtnClk(connectBtn, token, client):
    print("Connect/disconnect button pressed")
    if connectBtn.cget('text') == "Connect bot to discord":
        print("Connecting")
        await client.start(token)
        connectBtn.configure(text="Disconnect bot from discord")
    else:
        print("Disconnecting")
        connectBtn.configure(text="Connect bot to discord")

async def test():
    print("staring test")
    await asyncio.sleep(1)
    print("finished test")

async def myLoop():
    while True:
        "print hi"