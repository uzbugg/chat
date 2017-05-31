#!/usr/bin/python3
import tkinter as tk
import threading
import time
import socket
import json
import sys

class Interface(tk.Frame):
    def __init__(self, core = None):

        #Frame, packer, instatiation of GUI parts
        tk.Frame.__init__(self, core,  width=388, height = 512, )
        self.pack()
        # Window for incomming messages
        self.receiver()
        # input text a.k.a send a message
        self.sender()
        self.userList()

    # WINDOW FOR DISPALY MESSAGES
    def receiver(self):
        window = tk.Frame(self, bg="#0d0f0d", highlightbackground="#26ed0b")
        window['relief'] = 'solid'
        window.grid(row=1, sticky = 'W')
        self.text = tk.Text(window, width=50, height=28, bg="#0d0f0d",  fg="#26ed0b", borderwidth=0,highlightbackground="#26ed0b", highlightthickness=8, wrap="word")
        self.text['font'] = "Helvetica 11 "
        scroll = tk.Scrollbar(window, command=self.text.yview,relief='groove',borderwidth=0,highlightbackground="#26ed0b", highlightthickness=8,  orient = 'vertical' )
        self.text.config(yscrollcommand = scroll.set, state='disabled')
        self.text.pack(side = 'left', fill= 'both')
        scroll.pack(side = 'right', fill = 'y')
        #start threading - recieving messages
        threading.Thread(target=self.getMsg).start()

    #MESSAGE INPUT WINDOW
    def sender(self):
        #type text
        inpt = tk.Frame(self, bg="#0d0f0d", borderwidth=0)
        inpt['relief'] = 'solid'
        inpt.grid(row = 2, sticky = 'W')
        #tex frame
        self.msg = tk.Text(inpt, width = 60, height = 2, bg="#0d0f0d", fg="green",borderwidth=0,highlightbackground="#26ed0b", highlightthickness=8, wrap="word")
        self.msg.config(insertbackground="#26ed0b")
        self.msg['fg'] ='#26ed0b'
        self.msg['font'] = "Helvetica 9 "
        self.msg.insert('1.0', 'here... ')
        sideBar = tk.Scrollbar(inpt, command = self.msg.yview, orient = 'vertical')

        self.msg.config(yscrollcommand = sideBar.set)
        self.msg.pack(side = 'left', fill="both")

        sideBar.pack(side = 'right', fill = 'y')

        self.msg.bind('<Return>', self.sendMsg)
        self.msg.delete(1.0, tk.END)

    def getMsg(self):

        numlines = self.text.index(tk.END).split('.')[0]
        self.text['state'] = 'normal'

        if numlines == 100:
            self.text.delete('1.0', '2.0')

            message = data[0]['nick'] +  ": " + data[1]['msg'] + "\n"
            self.text.insert(tk.END, message)
            self.text.see = tk.END
            self.text['state'] = 'disabled'

        message = data[0]['nick'] +  ": " + data[1]['msg'] + "\n"
        self.text.insert(tk.END, message)
        self.text.see = tk.END
        self.text['state'] = 'disabled'

    #chat client-side functionZ
    def sendMsg(self, callback):
        print(callback)
        message = self.msg.get('1.0', tk.END)
        self.msg.delete('1.0', tk.END)


root = tk.Tk()
root.title("StetChat")
#root.geometry("450x500")
Chat = Interface(core = root)
Chat.mainloop()
