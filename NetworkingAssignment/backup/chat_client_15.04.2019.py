import socket
import sys
import time
import threading
import asciiart

debug = 0

def msgserver(sHost, sPort, msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        sys.exit('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])

    if debug == 1: print 'MSGSERVER: Socket Created'
    try:
        s.connect((sHost, sPort))
    except:
        sys.exit('Server OFFLINE. Exiting')

    if debug == 1: print 'MSGSERVER: Socket Connected to server ' + sHost + ' on port ' + str(sPort)

    try:
        s.sendall(msg)
    except socket.error:
        sys.exit('Send failed')
    time.sleep(80.0 / 1000.0)
    reply = s.recv(4096)
    if msg.split('|')[0] == 'REGISTER':
        if reply != 'OK':
            if reply == 'Nickname already present':
                sys.exit('Nickname already registered on server. Exiting.')
            sys.exit('Nickname already registered on server. Exiting.')
        else:
            print 'Registered successfully with the server'

    if msg.split('|')[0] == 'SEARCH':
        if reply == 'ERROR':
            print('USER Not found. Probably offline??')
        else:
            user_info = reply.split('|')
            print('USER found. IP ' + user_info[1] + ' Port ' + user_info[2])
            return user_info

    if msg.split('|')[0] == 'USERS':
        print(reply)

    s.close()


def udpServer(usHost, usPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((usHost, usPort))
    while True:
        data, addr = sock.recvfrom(1024)
        if data == 'PING?PONG':
            sock.sendto('PONG?PING', (addr[0], addr[1]))
            print 'Received message: ', data
        if data == 'FREEFORCHAT' and not onchat:
            sock.sendto('STARTCHAT', (addr[0], addr[1]))
            print 'Received message: ', data


def udpClient(target_IP, target_PORT, target_Message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(target_Message, (target_IP, target_PORT))
    data, addr = sock.recvfrom(1024)
    if target_Message == 'FREEFORCHAT' and data == 'STARTCHAT':
        print "received message:", data


server_host = '127.0.0.1'
server_port = 8888
# print('Welcome to SuperChat Server\r\nStage 1: Now registering the client with the server...\r\n')
print asciiart.comando_welcome
print('Stage 1: Registering with the Server')
# message = 'REGISTER|' + sys.argv[1] + '|' + sys.argv[2] + '|' + sys.argv[3]
message = 'REGISTER|doubleG|127.0.0.1|7777'
msgserver(server_host, server_port, message)
time.sleep(300.0 / 1000.0)

print('Stage 2: starting UDP Server')
usHost = '127.0.0.1'
usPort = 7777
t1 = threading.Thread(target=udpServer, args=(usHost, usPort))
t1.setDaemon(True)
t1.start()

while True:
    input = raw_input('Messaggio: ')
    print 'ok: ' + input + '\n'
    if input.split()[0] == '!help':
        print asciiart.fg.YELLOW + asciiart.style.BRIGHT + asciiart.comando_help + asciiart.fg.WHITE

    if input.split()[0] == '!connect':
        print asciiart.fg.YELLOW + asciiart.style.BRIGHT + 'Starting Chat with ' + input.split()[1] + asciiart.fg.WHITE
        try:
            info_utente = msgserver(server_host, server_port, 'SEARCH|' + input.split()[1])
            print 'Connecting with the user...'
            onchat = True
        except:
            print "Can't open a chat with this user"

    if input.split()[0] == '!show':
        print asciiart.fg.YELLOW + asciiart.style.BRIGHT + 'Requesting User List from the server.. \r\n\r\n' + asciiart.fg.WHITE
        try:
            users_list = msgserver(server_host, server_port, 'USERS|')
        except:
            print "Can't open a chat with this user"

    if input.split()[0] == '!quit':
        print asciiart.fg.BLUE + asciiart.style.BRIGHT + 'DEREGISTERING NickName from Server'
        # message = 'DEREGISTER|' + sys.argv[1]
        message = 'DEREGISTER|doubleG'
        msgserver(server_host, server_port, message)
        sys.exit('Quitting...Bye Bye')

    if input.split()[0][0] == '!':
        print 'Command not available'

