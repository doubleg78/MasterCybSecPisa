#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:14:59 2019

@author: user
"""

import socket   # <-- socket
import sys      # <-- for exit

def sendmessage(iphost, porthost, msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()
    s.connect((iphost, porthost))  # <-- TUPLA!!
    # connect e' bloccante in attesa che venga effettuata la connessione (pero' minore)
    print 'Socket Connected to ' + s.getsockname()[0] + ' on ip ' + iphost

    try:
        s.sendall(msg)  # <-- Unico argomento il messaggio da inviare
    # sendall e' anche questa bloccante
    except socket.error:
        print 'Send failed'
        sys.exit()

    reply = s.recv(4096)    # Argomento un intero grandezza in bytes del buffer che l'OS alloca per ricevere dati
    # recv detta anche bloccante in quanto rimane in ascolto per la ricezione della richiesta
    print reply
    s.close()


host = 'www.google.it'

try:
    remoteip = socket.gethostbyname('www.google.it')
except socket.gaierror:
    print 'Hostname could not be resolved. Exiting.'
    sys.exit()
print 'Ip address of ' + host + ' is ' + remoteip

sendmessage(remoteip, 80, 'GET / HTTP/1.1\r\n\r\n')



