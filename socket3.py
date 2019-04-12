#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 19:13:13 2019

@author: user
"""

import socket   # <-- socket
import sys      # <-- for exit
import time


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
conn, addr = s1.accept()

while True:
    #conn, addr = s1.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    #MessaggioBevenuto = 'Ciao Amico mio\nscrivimi qualcosa che\ncome un pappagallo\nte lo ripeto....'
    MessaggioBenvenuto1 = '   _____  _____    _____ _    _ _____  ______ _____   _____ _    _       _______ \n\r  / ____|/ ____|  / ____| |  | |  __ \|  ____|  __ \ / ____| |  | |   /\|__   __|\n\r | |  __| |  __  | (___ | |  | | |__) | |__  | |__) | |    | |__| |  /  \  | |   \n\r | | |_ | | |_ |  \___ \| |  | |  ___/|  __| |  _  /| |    |  __  | / /\ \ | |   \n\r | |__| | |__| |  ____) | |__| | |    | |____| | \ \| |____| |  | |/ ____ \| |   \n\r  \_____|\_____| |_____/ \____/|_|    |______|_|  \_\\______|_|  |_/_/    \_\_|   \n\r                                                                                 \n\r                                                                                \n\r'
    MessaggioBenvenuto2 = "\n\r  _____                     _____      _     _       \n\r |_   _|                   |  __ \    | |   | |      \n\r   | |     __ _ _ __ ___   | |__) |_ _| |__ | | ___  \n\r   | |    / _` | '_ ` _ \  |  ___/ _` | '_ \| |/ _ \ \n\r  _| |_  | (_| | | | | | | | |  | (_| | |_) | | (_) |\n\r |_____|  \__,_|_| |_| |_| |_|   \__,_|_.__/|_|\___/ \n\r                                                     \n\r                                                     \n\r"
    MessaggioBenvenuto3 = '\n\r\n\r+-------------------------------------------------+\n\r| WELCOME TO THE SUPER SECRET CHATBOX             |\n\r|                                                 |\n\r| PLEASE HANG FOR THE MENU AND CHOOSE YOUR PILL   |\n\r|                                                 |\n\r| BLUE PILL                                       |\n\r| The story ends, you wake up in your bed and     |\n\r| believe whatever you want to believe            |\n\r|                                                 |\n\r| RED PILL                                        |\n\r| You stay in Wonderland, and I show you how      |\n\r| deep the rabbit hole goes                       |\n\r|                                                 |\n\r+-------------------------------------------------+\n\r'
    MessaggioBenvenuto4 = '+-------------------------------------------------+\n\r' \
                          '|                                                 |\n\r' \
                          '|               TAKE YOUR DECISION                |\n\r' \
                          '|                                                 |\n\r' \
                          '| 1) Blue Pill (Exit)                             |\n\r' \
                          '|                                                 |\n\r' \
                          '| 2) Easy Red Pill (no cryptochat)                |\n\r' \
                          '|                                                 |\n\r' \
                          '| 3) Medium Red Pill (shared key cryptochat)      |\n\r' \
                          '|                                                 |\n\r' \
                          '| 4) Hard Red Pill (RSA cryptochat)               |\n\r' \
                          '|                                                 |\n\r' \
                          '|                                                 |\n\r' \
                          '+-------------------------------------------------+\n\r' \
                          'Type your selection [1 2 3 4]: '
    conn.sendall(MessaggioBenvenuto1)
    time.sleep(1)
    #conn.sendall(MessaggioBenvenuto2)
    #time.sleep(1)
    conn.sendall(MessaggioBenvenuto3)
    time.sleep(1)
    conn.sendall(MessaggioBenvenuto4)
    time.sleep(1)
    data = conn.recv(1024)
    if data == '1\r\n':
        conn.sendall('Hug and Kiss baby. See you next time.\r\n')
        #conn.close()
    reply = 'OK...' + data
    conn.sendall(reply)



