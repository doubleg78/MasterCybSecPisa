import socket
import time
import threading
import asciiart
import sys


debug = 0

#  Color shortcut for printing in various Color
def error_message(msg):
    return asciiart.fg.RED + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


def infoY_message(msg):
    return asciiart.fg.YELLOW + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


def infoC_message(msg):
    return asciiart.fg.CYAN + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


def infoG_message(msg):
    return asciiart.fg.GREEN + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


def infoW_message(msg):
    return asciiart.fg.WHITE + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


def infoB_message(msg):
    return asciiart.fg.BLUE + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


def msgserver(sHost, sPort, msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        sys.exit('Failed to create socket. Error code: ' + str(socket.error))

    print infoC_message('MSGSERVER: Socket Created') if debug == 1 else '',
    try:
        s.connect((sHost, sPort))
    except:
        sys.exit('Server OFFLINE. Exiting')

    print infoC_message('MSGSERVER: Socket Connected to server ' + sHost + ' on port ' + str(sPort)) if debug == 1 else '\r',

    try:
        s.sendall(msg)
    except socket.error:
        sys.exit('Send failed')

    time.sleep(80.0 / 1000.0)
    reply = s.recv(4096)

    #  REGISTERING NICK IP AND PORT TO SERVER AND CHECK IF NICKNAME IS ALREADY TAKEN
    if msg.split('|')[0] == 'REGISTER':
        if reply != 'OK':
            if reply == 'Nickname already present':
                sys.exit('Nickname already registered on server. Exiting.')
            sys.exit('Nickname already registered on server. Exiting.')
        else:
            # print infoG_message('Registered successfully with the server')
            print infoB_message(asciiart.messaggio_registration_ok)

    #  SEARCH IP AND PORT OF AN USER TO CHAT WITH
    if msg.split('|')[0] == 'SEARCH':
        if reply == 'ERROR':
            print error_message('USER Not found. Probably offline??')
            return False
        else:
            user_info = reply.split('|')
            print infoG_message('USER found. IP ' + user_info[1] + ' Port ' + user_info[2])
            return user_info

    #  REQUEST LIST OF USERS FROM SERVER
    if msg.split('|')[0] == 'USERS':
        print(reply)

    # s.close()


def udpServer(usHost, usPort):
    global onchat, onchat_ip, onchat_port
    global command_msg
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((usHost, usPort))
    while True:

        try:
            data, addr = sock.recvfrom(1024)
        except:
            sys.stdout.write(error_message('ERRORE RICEZIONE DATI'))
            sys.stdout.write('\r'+command_msg)
            return

        if data == 'PING?PONG':
            sock.sendto('PONG?PING', (addr[0], addr[1]))

        # MESSAGE START_CHAT|<usernick>|<remotenick>|<userIP>|<userPORT>
        if data.split('|')[0] == 'START_CHAT' and not onchat:
            sock.sendto('CHAT_OK', (addr[0], addr[1]))
            onchat = data.split('|')[1]
            onchat_ip = data.split('|')[3]
            onchat_port = int(data.split('|')[4])
            command_msg = infoG_message('[' + usNick + ' #]: ')
            sys.stdout.write("\r")
            sys.stdout.flush()
            sys.stdout.write(infoG_message('Received message: ' + data + '\n'))
            sys.stdout.write(infoY_message('Now Chatting with ' + onchat + '\n'))
            sys.stdout.write('\r'+command_msg)
            sys.stdout.flush()

        # CHECK IF NEW CHAT IS REQUESTED BUT USER STILL ONLINE WITH SOMEONE ELSE
        if data.split('|')[0] == 'START_CHAT' and onchat != False:
            sock.sendto('KO_CHAT', (addr[0], addr[1]))

        if data.split('|')[0] == 'END_CHAT' and onchat != False:
            sock.sendto('END_OK|' + usNick, (addr[0], addr[1]))
            onchat = False
            onchat_ip = ''
            onchat_port = 0
            command_msg = infoW_message('[Command: #] ')
            sys.stdout.write("\r")
            sys.stdout.flush()
            sys.stdout.write(infoG_message('Received message: ' + data + '\n'))
            sys.stdout.write(infoY_message('Ending chat with ' + data.split('|')[1] + '\n'))
            sys.stdout.write('\r'+command_msg)
            sys.stdout.flush()

        # FORMAT: MSG|<remotenick>|<usernick>|<message sent>
        if data.split('|')[0] == 'MSG' and onchat != False and onchat == data.split('|')[1]:
            sock.sendto('MSG_ACK|' + usNick, (addr[0], addr[1]))
            sys.stdout.write("\r")
            sys.stdout.flush()
            sys.stdout.write(''.join([infoW_message('.:-{ '), infoY_message(data.split('|')[1]), infoW_message(' }-:. '), infoY_message(data.split('|')[3])]))
            sys.stdout.write('\n'+command_msg)
            sys.stdout.flush()


def udpClient(target_IP, target_PORT, target_Message):
    global onchat, onchat_ip, onchat_port
    global command_msg
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(target_Message, (target_IP, target_PORT))
    try:
        data, addr = sock.recvfrom(1024)
    except:
        if target_Message.split('|')[0] == 'MSG':
            print error_message("Can't send message. User offline now? Try disconnect and reconnect.")
            sock.close()
            return
        if target_Message.split('|')[0] == 'END_CHAT':
            data = 'END_OK'

    if target_Message.split('|')[0] == 'START_CHAT' and data == 'CHAT_OK':
        sys.stdout.write("\nUDPCLIENT received message:" + data + '\n')
        onchat = target_Message.split('|')[2]
        onchat_ip = target_IP
        onchat_port = int(target_PORT)
        command_msg = infoC_message('[' + target_Message.split('|')[1] + ' #]: ')
        sys.stdout.write(infoY_message('Now Chatting with ' + onchat + '\n'))
        sys.stdout.flush()

    if target_Message.split('|')[0] == 'START_CHAT' and data == 'KO_CHAT':
        print error_message('User ' + target_Message.split('|')[2] + ' already on chat. Try again later!')

    if target_Message.split('|')[0] == 'END_CHAT' and data.split('|')[0] == 'END_OK':
        sys.stdout.write(infoG_message("\nUDPCLIENT received message:" + data + '\n'))
        onchat = False
        onchat_ip = ''
        onchat_port = 0
        command_msg = infoW_message('[Command: #] ')
        sys.stdout.write(infoG_message('Chat ENDED with ' + target_Message.split('|')[2] + '\n'))
        sys.stdout.flush()

    if target_Message.split('|')[0] == 'MSG' and data.split('|')[0] == 'MSG_ACK':
        sys.stdout.flush()
    #sock.close()


server_host = '127.0.0.1'
server_port = 8888

time.sleep(300.0 / 1000.0)
if len(sys.argv) >= 4:
    usNick = sys.argv[1]
    usHost = sys.argv[2]
    usPort = int(sys.argv[3])
    if (len(sys.argv) == 5) and (sys.argv[4] == '--debug'): debug = 1
else:
    # sys.exit('Not Enough parameter. Start program with python <program.py> <NickName> <ip-address> <port>')
    print error_message('Not enough parameters.')
    print infoY_message('Usage: chat_client.py nickname your_ip_address your_ip_port [--debug]')
    print infoB_message('Falling back anyway to default: Nickname=doubleG IP=127.0.0.1 PORT=7777')
    usNick = 'doubleG'
    usHost = '127.0.0.1'
    usPort = 7777

print infoB_message(asciiart.messaggio_welcome)
print infoY_message('Stage 1: Registering with the Server')
#  Send registration message to the server. Format: REGISTER|<userNick>|<userHost>|<userPort>
message = '|'.join(['REGISTER', usNick, usHost, str(usPort)])
msgserver(server_host, server_port, message)
time.sleep(300.0 / 1000.0)

print infoY_message('Stage 2: starting UDP Server')
t1 = threading.Thread(target=udpServer, args=(usHost, usPort))
t1.setDaemon(True)
t1.start()

# print infoG_message('Client Ready!')
print infoB_message(asciiart.messaggio_client_ready)

onchat = False
onchat_ip = ''
onchat_port = 0
command_list = ['!help', '!connect', '!disconnect', '!show', '!quit']
command_msg = '[Command: #] '

while True:
    time.sleep(0.03)
    uInput = raw_input(infoW_message(command_msg)).split()
    if len(uInput) != 0:
        if uInput[0].lower() == '!help':
            print infoY_message(asciiart.comando_help)

        if uInput[0].lower() == '!connect':
            if onchat != False:
                print error_message('Currently on chat with ' + onchat + '!!')
                print infoG_message('Please disconnect first! ')
            else:
                if len(uInput) <= 1:
                    print error_message('You must specify a user to connect.')
                else:
                    print infoY_message('Starting Chat with ' + uInput[1])
                    try:
                        info_utente = msgserver(server_host, server_port, 'SEARCH|' + uInput[1])
                        if info_utente != False:
                            print infoY_message('Connecting with the user...')
                            #MESSAGE START_CHAT|<usernick>|<remotenick>|<userIP>|<userPORT>
                            mess = ''.join(['START_CHAT', '|', usNick, '|', uInput[1], '|', usHost, '|', str(usPort)])
                            t2 = threading.Thread(target=udpClient, args=(info_utente[1], int(info_utente[2]), mess))
                            t2.setDaemon(True)
                            t2.start()
                    except:
                        print error_message("Can't open a chat with this user")

        if uInput[0].lower() == '!disconnect':
            print infoG_message('Disconnecting current chat...')
            if onchat:
                #t2 = threading.Thread(target=udpClient, args=(info_utente[1], int(info_utente[2]), 'END_CHAT|' + usNick + '|' + onchat))
                t2 = threading.Thread(target=udpClient, args=(onchat_ip, onchat_port, 'END_CHAT|' + usNick + '|' + onchat))
                t2.setDaemon(True)
                t2.start()
            else:
                print error_message('ERROR: you are not currently on any chat\r\n')

        if uInput[0].lower() == '!show':
            print infoY_message('Requesting User List from the server.. \r\n')
            try:
                users_list = msgserver(server_host, server_port, 'USERS|')
            except:
                print error_message('ERROR: server offline?!')

        if uInput[0].lower() == '!quit':
            print infoG_message('DEREGISTERING NickName from Server')
            # message = 'DEREGISTER|<userNick>'
            message = 'DEREGISTER|' + usNick
            msgserver(server_host, server_port, message)
            if onchat != False:
                t2 = threading.Thread(target=udpClient, args=(onchat_ip, onchat_port, 'END_CHAT|' + usNick + '|' + onchat))
                t2.setDaemon(True)
                t2.start()
                t2.join(1)
            sys.exit('Quitting...Bye Bye')

        if uInput[0][0] == '!' and uInput[0].lower() not in command_list:
            print error_message('Command not available.\r\nPlease check command with !help\r\n')

        if uInput[0][0] != '!' and onchat != False:
            #FORMAT: MSG|<usernick>|<remotenick>|<message to send>
            chat_mess = ''.join(['MSG', '|', usNick, '|', onchat, '|', ' '.join(uInput)])
            t2 = threading.Thread(target=udpClient, args=(onchat_ip, onchat_port, chat_mess))
            t2.setDaemon(True)
            t2.start()

