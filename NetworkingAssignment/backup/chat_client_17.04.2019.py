import socket
import sys
import time
import threading
import asciiart
import codecs

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
            return False
        else:
            user_info = reply.split('|')
            print('USER found. IP ' + user_info[1] + ' Port ' + user_info[2])
            return user_info

    if msg.split('|')[0] == 'USERS':
        print(reply)

    s.close()


def udpServer(usHost, usPort):
    global onchat, onchat_ip, onchat_port
    global command_msg
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((usHost, usPort))
    while True:
        data, addr = sock.recvfrom(1024)
        if data == 'PING?PONG':
            sock.sendto('PONG?PING', (addr[0], addr[1]))
            print 'Received message: ', data
        #MESSAGE START_CHAT|<usernick>|<remotenick>|<userIP>|<userPORT>
        if data.split('|')[0] == 'START_CHAT' and not onchat:
            sock.sendto('CHAT_OK', (addr[0], addr[1]))
            onchat = data.split('|')[1]
            onchat_ip = data.split('|')[3]
            onchat_port = int(data.split('|')[4])
            command_msg = '[' + usNick + ' #]: '
            sys.stdout.write("\r")
            sys.stdout.flush()
            sys.stdout.write('Received message: ' + data + '\n')
            sys.stdout.write('Now Chatting with ' + onchat + '\n')
            sys.stdout.write('\r'+command_msg)
            sys.stdout.flush()
        if data.split('|')[0] == 'END_CHAT' and onchat != False:
            sock.sendto('END_OK|' + usNick, (addr[0], addr[1]))
            onchat = False
            onchat_ip = ''
            onchat_port = 0
            command_msg = '[Command: #]'
            sys.stdout.write("\r")
            sys.stdout.flush()
            sys.stdout.write('Received message: ' + data + '\n')
            sys.stdout.write('Ending chat with ' + data.split('|')[1] + '\n')
            sys.stdout.write('\r'+command_msg)
            sys.stdout.flush()
        # FORMAT: MSG|<remotenick>|<usernick>|<message sent>
        if data.split('|')[0] == 'MSG' and onchat != False and onchat == data.split('|')[1]:
            sock.sendto('MSG_ACK|' + usNick, (addr[0], addr[1]))
            sys.stdout.write("\r")
            sys.stdout.flush()
            sys.stdout.write(''.join(['[', asciiart.fg.BLUE, data.split('|')[1], ' -->] ', data.split('|')[3], asciiart.fg.RESET]))
            sys.stdout.write('\n'+command_msg)
            sys.stdout.flush()


def udpClient(target_IP, target_PORT, target_Message):
    global onchat, onchat_ip, onchat_port
    global command_msg
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(target_Message, (target_IP, target_PORT))
    data, addr = sock.recvfrom(1024)
    if target_Message.split('|')[0] == 'START_CHAT' and data == 'CHAT_OK':
        sys.stdout.write("\nUDPCLIENT received message:" + data + '\n')
        onchat = target_Message.split('|')[2]
        onchat_ip = target_IP
        onchat_port = int(target_PORT)
        command_msg = '[' + target_Message.split('|')[1] + ' #]: '
        sys.stdout.write('Now Chatting with ' + onchat + '\n')
        sys.stdout.flush()
    if target_Message.split('|')[0] == 'END_CHAT' and data.split('|')[0] == 'END_OK':
        sys.stdout.write("\nUDPCLIENT received message:" + data + '\n')
        onchat = False
        onchat_ip = ''
        onchat_port = 0
        command_msg = '[Command: #]'
        sys.stdout.write('Chat ENDED with ' + target_Message.split('|')[2] + '\n')
        sys.stdout.flush()
    if target_Message.split('|')[0] == 'MSG' and data.split('|')[0] == 'MSG_ACK':
        sys.stdout.flush()
    sock.close()


server_host = '127.0.0.1'
server_port = 8888

print asciiart.comando_welcome
print('Stage 1: Registering with the Server')
time.sleep(300.0 / 1000.0)
if len(sys.argv) == 4:
    usNick = sys.argv[1]
    usHost = sys.argv[2]
    usPort = int(sys.argv[3])
else:
    #sys.exit('Not Enough parameter. Start program with python <program.py> <NickName> <ip-address> <port>')
    usNick = 'doubleG'
    usHost = '127.0.0.1'
    usPort = 7777

message = 'REGISTER|' + usNick + '|' + usHost + '|' + str(usPort)
msgserver(server_host, server_port, message)
time.sleep(300.0 / 1000.0)

print('Stage 2: starting UDP Server')
t1 = threading.Thread(target=udpServer, args=(usHost, usPort))
t1.setDaemon(True)
t1.start()

onchat = False
onchat_ip = ''
onchat_port = 0
command_list = ['!help', '!connect', '!disconnect', '!show', '!quit']
command_msg = '[Command: #]'

while True:
    time.sleep(0.05)
    input = raw_input(command_msg)
    if input != '':
        if input.split()[0].lower() == '!help':
            print asciiart.fg.YELLOW + asciiart.style.BRIGHT + asciiart.comando_help + asciiart.fg.WHITE

        if input.split()[0].lower() == '!connect':
            if onchat != False:
                print asciiart.fg.YELLOW + asciiart.style.BRIGHT + 'Currently on chat with ' + onchat + '!!' + asciiart.fg.WHITE
                print asciiart.fg.YELLOW + asciiart.style.BRIGHT + 'Please disconnect first! ' + asciiart.fg.WHITE
            else:
                print asciiart.fg.YELLOW + asciiart.style.BRIGHT + 'Starting Chat with ' + input.split()[1] + asciiart.fg.WHITE
                try:
                    info_utente = msgserver(server_host, server_port, 'SEARCH|' + input.split()[1])
                    if info_utente != False:
                        print 'Connecting with the user...'
                        #MESSAGE START_CHAT|<usernick>|<remotenick>|<userIP>|<userPORT>
                        mess = ''.join(['START_CHAT', '|', usNick, '|', input.split()[1], '|', usHost, '|', str(usPort)])
                        t2 = threading.Thread(target=udpClient, args=(info_utente[1], int(info_utente[2]), mess))
                        t2.setDaemon(True)
                        t2.start()
                except:
                    print "Can't open a chat with this user"

        if input.split()[0].lower() == '!disconnect':
            print asciiart.fg.YELLOW + asciiart.style.BRIGHT + 'Disconnecting current chat...' + asciiart.fg.WHITE
            if onchat:
                #t2 = threading.Thread(target=udpClient, args=(info_utente[1], int(info_utente[2]), 'END_CHAT|' + usNick + '|' + onchat))
                t2 = threading.Thread(target=udpClient, args=(onchat_ip, onchat_port, 'END_CHAT|' + usNick + '|' + onchat))
                t2.setDaemon(True)
                t2.start()
            else:
                print asciiart.fg.RED + asciiart.style.BRIGHT + \
                      'ERROR: you are not currently on any chat\r\n\r\n' \
                      + asciiart.fg.RESET + asciiart.style.RESET_ALL

        if input.split()[0].lower() == '!show':
            print asciiart.fg.YELLOW + asciiart.style.BRIGHT + \
                  'Requesting User List from the server.. \r\n\r\n' \
                  + asciiart.fg.WHITE
            try:
                users_list = msgserver(server_host, server_port, 'USERS|')
            except:
                print "ERROR: server offline?!"

        if input.split()[0].lower() == '!quit':
            print asciiart.fg.BLUE + asciiart.style.BRIGHT + 'DEREGISTERING NickName from Server'
            # message = 'DEREGISTER|' + sys.argv[1]
            message = 'DEREGISTER|' + usNick
            msgserver(server_host, server_port, message)
            sys.exit('Quitting...Bye Bye')

        if input.split()[0][0] == '!' and input.split()[0].lower() not in command_list:
            print asciiart.fg.RED + asciiart.style.BRIGHT + 'Command not available.\r\nPlease check command with !help\r\n' + asciiart.fg.RESET + asciiart.style.RESET_ALL

        if input.split()[0][0] != '!' and onchat != False:
            #FORMAT: MSG|<usernick>|<remotenick>|<message to send>
            chat_mess = ''.join(['MSG', '|', usNick, '|', onchat, '|', input])
            t2 = threading.Thread(target=udpClient, args=(onchat_ip, onchat_port, chat_mess))
            t2.setDaemon(True)
            t2.start()

