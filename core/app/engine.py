#!/usr/bin/python3
import socket
import threading
import time
import json
import sys

class Engine():
    def __init__(self):

        self.sock = 0 #socket
        self.connections = [] #list of ip's
        self.udata = {} #usr data
        self.buffer = {} #mesage buffer

    def createServer(self, ip, port, socktype = 'udp'):
        #try-except?
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((socket.gethostname(), port))
        return 1

    def get(self):
        data, addr = self.sock.recvfrom(1024)
        return data, addr

    #sends to onc client
    def post(self, data, client):
        '''
        data is the data to be sent ofc
        client is a list (ip, port)
        '''
        self.sock.sendto(data.encode("utf-8"), client)

    #broadcast the message
    def broadcast(self, data):
        if data:
            for conn in self.connections:
                self.post(data, conn)
            return 1
        else:
            return 0

    #saves idetificators from incomming connections
    #that way it's possible to keep track of some `user list`
    def onconnect(self, address):
        if address not in self.connections:
            self.connections.append(address)
            uid = address[0] + ':' + str(address[1]) #special ID, if user cant be accessed delete u data also
            entry = {}
            #entry['port'] = address[1] #?
            entry['time'] = time.time()
            self.udata[uid] = entry

    #incomming messages go into a special buffer
    #the processing of each message comes later in order
    #as the messages appear in the buffer
    def msgbuffer(self, address, data):
        length = len(self.buffer)
        tmp = {
            'data': data,
            'addr': address
        }
        #len should return real length +1 or 0
        self.buffer[length] = tmp
        tmp = None

    #check the dictionary of messages in the buffer
    # process them and also sends each messages(broadcast)
    #afterwards a messages is deleted from the buffer
    def bufferProc(self):
        while 1:
            if self.buffer:
                for i in range(0, len(self.buffer)):
                    self.onconnect(self.buffer[i]['addr'])
                    #since the server can get 'special command'
                    #here we will handle them
                    self.buffer[i]['data'] = self.buffer[i]['data'].decode("utf-8")
                    if self.buffer[i]['data'][0] == '/':
                        self.switch(self.buffer[i]['data'],self.buffer[i]['addr'])
                        self.buffer[i]['data'] = None
                    #broadcast should not send None type, so yeah
                    self.broadcast(self.buffer[i]['data'])
                    del self.buffer[i]

    #probabbly just updates the 'last-seen' time of a client
    def ping(self, client):
        uid = client[0] + ':' + str(client[1])
        newtime = time.time()
        try:
            self.udata[uid]['time'] = newtime
            #self.pong(client)
        except KeyError:
            pass

    #to keep up...
    def pong(self, remote):
        self.post('1', remote)

    #it just checks the current user list
    #probabbly shit implementation
    def clientCheck(self):
        while 1:
            for c in self.connections:
                uid = c[0] + ":" + str(c[1])
                cltime = self.udata[uid]['time']

                if time.time() - float(cltime) >= 30:
                    self.post('/ping', c)
                    wait = time.time()
                    while 1:
                        #has the time changed? break.
                        if cltime != self.udata[uid]['time']:
                            break
                        #too long? break.
                        if time.time() - float(wait) >= 30:
                            break
                    #time still the same? this client is not here :/
                    if float(cltime) == self.udata[uid]['time']:
                        #send bye message
                        self.post("/bye", c)
                        self.connections.remove(c)
                        del self.udata[uid]
                        print("removed " + str(c))
        time.sleep(30)

    #so that the server can process addational commands
    #side note: the actual command should come in data param as the message does??
    def switch(self, do, arg):
        options = {
            "pong" : self.pong,
            "ping" : self.ping,
        }

        if do[1:] in options:
            options[do[1:]](arg)
        else:
            pass
