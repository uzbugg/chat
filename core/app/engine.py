#!/usr/bin/python3
import socket
import threading
import time
import json
import sys

'''
Server
'''
class Engine():
    def __init__(self):

        self.sock = 0
        self.connections = []
        self.udata = {}

    def createServer(self, ip, port, socktype = 'udp'):

        if socktype == 'udp':

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((socket.gethostname(), port))

            return 1

        else:
            print("tcp not available yet")
            return 0

    def get(self):

        data, addr = self.sock.recvfrom(1024)
        if data.decode('utf-8')[0] == '/':
            self.switch(data.decode('utf-8'), addr)
            #if returned data, addr ?? - display action message
            return None, addr
        return data, addr

    '''
    sending bytes to single connections
    '''
    def post(self, data, client):
        '''
        data is the data to be sent ofc
        client is a list (ip, port)
        '''
        self.sock.sendto(data.encode('utf-8'), client)

    '''
    broadcasting - sending bytes to all connections
    '''
    def broadcast(self, data):
        for conn in self.connections:
            if  data:
                self.sock.sendto(data, conn)
            continue

    '''
    keeping track of active connnections
    '''
    def onconnect(self, new):
        if new not in self.connections:
            self.connections.append(new)
            uid = new[0] + ':' + str(new[1]) #special ID, if user cant be accessed delete u data also
            entry = {}
            entry['port'] = new[1]
            entry['time'] = time.time()
            self.udata[uid] = entry
    '''
    active connections watcher
    '''
    def ping(self, client):
        uid = client[0] + ':' + str(client[1])
        newtime = time.time()
        try:
            self.udata[uid]['time'] = newtime
            #self.pong(client)
        except KeyError:
            pass

    def pong(self, remote):
        self.post('1', remote)

    def clientCheck(self):
        while 1:
            for c in self.connections:
                uid = c[0] + ":" + str(c[1])
                cltime = self.udata[uid]['time']

                if time.time() - float(cltime) >= 30:
                    self.post('/ping', c)
                    wait = time.time()
                    while 1:
                        if cltime != self.udata[uid]['time']:
                            break
                        if time.time() >= float(cltime):
                            break
                    if float(cltime) == self.udata[uid]['time']:
                        self.connections.remove(c)
                        del self.udata[uid]

        time.sleep(30)

    def switch(self, do, arg):
        options = {
            "pong" : self.pong,
            "ping" : self.ping,
        }

        if do[1:] in options:
            options[do[1:]](arg)
        else:
            pass
