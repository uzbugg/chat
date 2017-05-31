#!/usr/bin/python
from core.client import Core
import threading
import json
import sys

class ClientZ:
    def __init__(self):
        self.core = Core()
        self.core.create('127.0.0.1', 8080)
        self.nick = 'r+'

        threading.Thread(target=self.SendMsg).start()
        threading.Thread(target=self.GetMsg).start()
        threading.Thread(target=self.core.ping()).start()

    def GetMsg(self):
        while 1:
            data = self.core.get()
            if not data:
                continue;
            data = json.loads(data)
            try:
                print(data[0]['nick'], ": ", data[1]['msg'])
            except ValueError:
                pass


    def SendMsg(self):
        while 1:
            message = input('-> ')
            msgObj = json.dumps([ { "nick": (self.nick) }, { "msg": (message)} ])
            self.core.post(msgObj)

    '''
    def switch(self, command):
        options = {
            "conn" : self.conn,
            "disconn" : self.disconn,
            "pong" : self.pong,
        }

        if command[1:] in options:
            options[command[1:]]()
        else:
            pass
    '''

cl = ClientZ()
