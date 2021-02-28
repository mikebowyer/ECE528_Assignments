import tkinter as tk
from lib import eventCallBacks




mainWindow = tk.Tk()

#Button
sendMsgBtn = tk.Button(
    text="Send a message",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=eventCallBacks.sendMsgBtnClk,
)
getUserInfoBtn = tk.Button(
    text="Get user information",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=eventCallBacks.getUserInfoBtnClk,
)
sendMsgBtn.pack()
getUserInfoBtn.pack()

mainWindow.mainloop()

