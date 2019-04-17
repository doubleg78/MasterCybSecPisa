import socket
import sys
import os
import time
import threading
import asciiart


def msgserver(sHost, sPort, msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        sys.exit('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])

    print 'MSGSERVER: Socket Created'
    try:
        s.connect((sHost, sPort))
    except:
        sys.exit('Server OFFLINE. Exiting')

    print 'MSGSERVER: Socket Connected to server ' + sHost + ' on port ' + str(sPort)

    try:
        s.sendall(msg)
    except socket.error:
        sys.exit('Send failed')
    time.sleep(1)
    reply = s.recv(4096)
    if msg.split('|')[0] == 'REGISTER' and reply != 'OK':
        if reply == 'Nickname already present':
            sys.exit('Nickname already registered on server. Exiting.')
        sys.exit('We have got problem registering to server. Exiting.')
    else:
        print 'Registered successfully with the server'

    s.close()


def udpServer(usHost, usPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((usHost, usPort))
    #options 1
    #t1 = threading.Thread(target=udpServerMessage, args=(sock,))
    #t1.start()
    #options 2
    udpServerMessage(sock)


def udpServerMessage(sock):
    while True:
        if stop_threads:
            break
        data, addr = sock.recvfrom(1024)
        if data == 'PING?PONG':
            sock.sendto('PONG?PING', (addr[0], addr[1]))
        print 'Received message: ', data


server_host = '127.0.0.1'
server_port = 8888
print('Welcome to SuperChat Server\r\nStage 1: Now registering the client with the server...\r\n')
#message = 'REGISTER|' + sys.argv[1] + '|' + sys.argv[2] + '|' + sys.argv[3]
message = 'REGISTER|doubleG|127.0.0.1|7777'
msgserver(server_host, server_port, message)
time.sleep(1)
print('Stage 2: starting UDP Server')
usHost = '127.0.0.1'
usPort = 7777
#options 1
#udpServer(usHost, usPort)
#options 2
stop_threads = False
t1 = threading.Thread(target=udpServer, args=(usHost, usPort))
t1.start()

while True:
    input = raw_input('Messaggio: ')
    print 'ok: ' + input + '\n'
    if input.split()[0] == '!help':
        print asciiart.comando_help
    if input.split()[0] == '!quit':
        #os._exit(1)
        stop_threads = True

        sys.exit('Quitting...Bye Bye')
