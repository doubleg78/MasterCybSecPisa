import socket
import sys
import time


def msgserver(sHost, sPort, msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        sys.exit('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])

    print 'MSGSERVER: Socket Created'

    s.connect((sHost, sPort))

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




server_host = '127.0.0.1'
server_port = 8888
print('Welcome to SuperChat Server\r\nNow registering the client with the server...\r\n')
#message = 'REGISTER|' + sys.argv[1] + '|' + sys.argv[2] + '|' + sys.argv[3]
message = 'REGISTER|doubleG|127.0.0.1|8880'
msgserver(server_host, server_port, message)
