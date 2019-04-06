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

    while 1:
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        MessaggioBevenuto = '###NASA SECRET SERVICE###\nSistema crittografico DSA\n\n##lascia ogni speranza##\n\nversa 4BTC per salvare la tua vita....'
        conn.sendall(MessaggioBevenuto)
        data = conn.recv(1024)
        reply = 'OK...\n\nper questa volta hai salva la vita \n\nma la prossima non sarà così semplice.\n\n' + data
        if not data:
            break
        
        conn.sendall(reply)
        conn.close()
        
    s.close()


serverecho('', 8889)

