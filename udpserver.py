 #!/usr/bin/python3
import threading
from core.app.engine import Engine
'''
UDP chat server
'''
class Chat():

    def __init__(self):
        self.Server = Engine()
        self.Server.createServer('', 8080, 'udp')
        threading.Thread(target=self.Server.bufferProc).start()
        threading.Thread(target=self.Server.clientCheck).start()
        self.loop()

    def loop(self):
        while 1:
            d, a = self.Server.get()
            self.Server.msgbuffer(a,d)
cl = Chat()
