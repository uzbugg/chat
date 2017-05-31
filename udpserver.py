#!/usr/bin/python3
import threading
from core.app.engine import Engine
'''
UDP chat server
'''
class Chat():

    def __init__(self):
        self.Server = Engine()
        self.Server.createServer('', 8000, 'udp')
        print(self.Server)
        threading.Thread(target=self.Server.clientCheck).start()
        self.loop()


    def loop(self):
        while 1:
            data, addr  = self.Server.get()
            print(addr)
            self.Server.onconnect(addr)
            print("adress is --> " + addr[0] + " || " + str(addr[1]))
            self.Server.broadcast(data)
            '''
            for conn in self.Server.connections:
                print(conn)

            print("_______________________")
            '''
            print(self.Server.udata)
            #print(data)
cl = Chat()
