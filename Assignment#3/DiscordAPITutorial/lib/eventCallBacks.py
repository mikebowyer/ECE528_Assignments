import tkinter as tk

def sendMsgBtnClk():
    print("send msessage button clicked")
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

def connectBtnClk(connectBtn):
    print("Connect/disconnect button pressed")
    if connectBtn.cget('text') == "Connect bot to discord":
        print("Connecting")
        connectBtn.configure(text="Disconnect bot from discord")
    else:
        print("Disconnecting")
        connectBtn.configure(text="Connect bot to discord")
