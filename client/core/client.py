#!/usr/bin/python
import socket
import time
import sys

'''
udp client for chat app.
notes(' try - except ')
'''
class Core:
    '''
    constructor
    notes(
        'nick support',
            )
    '''
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.remote = 0

    '''
    new server connection
    '''
    def create(self, host, port):
        self.remote = (host, port)

    '''
    receive data
    '''
    def get(self):
        data = self.sock.recv(1024)
        data = data.decode('utf-8')

        '''
        waiting for server response, add a function to let usr know srv is down and stuff u know
        '''
        if data == '/pong':
            data = None
            return data
        if data == '/ping':
            self.sock.sendto('/ping'.encode('utf-8'), self.remote)
            data = None
            return data

        return data

    '''
    get data
    '''
    def post(self, data):
        data = data.encode('utf-8')
        self.sock.sendto(data, self.remote)

    '''
    other tweakZZ
    '''
    def pong(self):
        data = '/pong'
        self.sock.sendto(data.encode('utf-8'), self.remote)

    def ping(self, rem = 0):
        data = '/ping'
        if rem == 1:
            self.sock.sendto(data.encode('utf-8'), self.remote)
            return 0

        while 1:
            self.sock.sendto(data.encode('utf-8'), self.remote)
            time.sleep(5)

    def disconnect(self):
        pass
