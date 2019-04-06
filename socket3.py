#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 19:13:13 2019

@author: user
"""

import socket   # <-- socket
import sys      # <-- for exit


def serverecho(bindip, portbind):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()

    try:
        s.bind((bindip, portbind))
    except socket.error, msg:
        print 'Bind failed. Error code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    s.listen(10)
    print 'Socket now listening'
    
    return s


#    check = raw_input('Avvio server (digitare exit per uscire)')
#    if check == "\n\n":
#        sys.exit()
s1 = serverecho('', 8888)

while True:
    conn, addr = s1.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    MessaggioBevenuto = 'Ciao Amico mio\nscrivimi qualcosa che\ncome un pappagallo\nte lo ripeto....'
    conn.sendall(MessaggioBevenuto)
    data = conn.recv(1024)
    reply = 'OK...' + data
    conn.sendall(reply)
    conn.close()

s1.close()

