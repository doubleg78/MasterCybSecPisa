import socket
import sys
from thread import *
import asciiart


debug = 0


def error_message(msg):
    return asciiart.fg.RED + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


def info_message(msg):
    return asciiart.fg.YELLOW + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


def infob_message(msg):
    return asciiart.fg.GREEN + asciiart.style.BRIGHT + msg + asciiart.fg.RESET + asciiart.style.RESET_ALL


# CHECK IF ARGS ARE CORRECTLY SPECIFIED. OTHERWISE PRINT ERROR AND REVERSE TO THE DEFAULT ONE
if len(sys.argv) == 2:
    HOST = str(sys.argv[1])
    PORT = str(sys.argv[2])
else:
    print error_message('No args specified or less/over the min/max')
    print infob_message('Command line: python chat_server.py <host> <port>')
    print error_message('Falling back to default value: HOST 127.0.0.1 PORT 8888\n')
    HOST = '127.0.0.1'
    PORT = 8888

# USER TABLE INITIALIZATION WITH COLUMN HEADER
user_table = [['NiCkNaMe', 'IP', 'PORT']]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print info_message('DEBUG: Socket created') if debug == 1 else ''

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print info_message('DEBUG: Bind failed. Error Code : ') + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print info_message('DEBUG: Socket bind complete') if debug == 1 else ''

# Start listening on socket
s.listen(100)
print info_message('DEBUG: Socket now listening') if debug == 1 else ''
# PRINTING THE WELCOME INFORMATION
print asciiart.comando_welcome_server
print infob_message('.:-[ SERVER READY ]-:.')
print info_message('--> Waiting connection... <--')


def client_thread(conn):
    # SUPPORT FUNCTION FOR PRINTING TO SCREEN THE USERS REGISTERED ON SERVER
    def show_users():
        for i, d in enumerate(user_table):
            line = '|'.join(str(x).ljust(22) for x in d)
            print(line)
            if i == 0:
                print('-' * len(line))

    data = conn.recv(1024)

    if data.split('|')[0] == 'REGISTER':  # USER REGISTRATION
        # msg format: REGISTER|<userNick>|<userIP>|<userPORT>
        print data if debug == 1 else ''
        client_request = data.split('|')
        result = adduser(client_request[1], client_request[2], client_request[3])
        if result == 'ADDED USER':
            conn.send('OK')  # IF ALL OK, SEND BACK THE 'OK' TO THE CLIENT
        if result == 'ERROR':
            conn.send('Nickname already present')  # PREVENT USER TO REGISTER WITH SOMEONE OTHER NICK STILL ALIVE
        conn.close()
        show_users()

    if data.split('|')[0] == 'DEREGISTER':  # DELETE USER REGISTRATION FROM SERVER
        # msg format: DEREGISTER|<userNick>
        print data if debug == 1 else ''
        client_request = data.split('|')
        if del_user(client_request[1]) == 'OK':
            print client_request[1] + ' User DeRegistered Successfully'
            show_users()

    if data.split('|')[0] == 'SEARCH':
        # msg format: SEARCH|<userNick>
        print data if debug == 1 else ''
        client_response = ''
        client_request = data.split('|')
        for x, users in enumerate(user_table):
            if users[0] == client_request[1]:
                if check_user_online(users[1], int(users[2])) == 'USER_ONLINE':  # FIRST CHECK IF USER IS STILL ONLINE
                    client_response = ('USERINFO|' + users[1] + '|' + users[2])
                    break
                else:
                    del_user(client_request[1])  # OTHERWISE DELETE USER FROM THE SYSTEM
                    client_response = 'ERROR'
                    break
        if client_response == '':  # FALL BACK FOR ANY OTHER GENERAL ERROR MAY OCCUR
            client_response = 'ERROR'
        conn.sendall(client_response)

    if data.split('|')[0] == 'USERS':  # GENERATE USERS LIST FOR THE CLIENT
        # msg format: USERS|
        print data if debug == 1 else ''
        client_response = ''
        for i, d in enumerate([i[0] for i in user_table]):
            if i == 0:
                client_response += (' ' * 10) + asciiart.fg.BLUE + asciiart.style.BRIGHT + d + '\r\n'
                client_response += (' ' * 10) + ('-' * 22) + '\r\n' + asciiart.style.RESET_ALL
            else:
                client_response += (' ' * 10) + asciiart.fg.YELLOW + asciiart.style.NORMAL + d + '\r\n' + asciiart.style.RESET_ALL
        print client_response
        conn.sendall(client_response)

    conn.close()


def adduser(cNick, cHost, cPort):
    for x, data in enumerate(user_table):
        if data[0] == cNick:
            print('REGISTER ERROR: User ' + cNick + ' already registered...checking if still alive')

            check = check_user_online(data[1], int(data[2]))

            if check == 'USER_OFFLINE':
                print('USER ' + cNick + ' Offline, deleting and registering new data')
                del user_table[x]
            else:
                print('USER ' + cNick + ' Online and registered with the server')
                return 'ERROR'
    user_table.append([cNick, cHost, cPort])
    return 'ADDED USER'


def check_user_online(UDP_IP, UDP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto('PING?PONG', (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024)
        print "received message:", data if debug == 1 else ''
        if data == 'PONG?PING':
            sock.close()
            return 'USER_ONLINE'
    except:
        sock.close()
        return 'USER_OFFLINE'


def del_user(user):
    for x, users in enumerate(user_table):
        if users[0] == user:
            del user_table[x]


while 1:
    conn, addr = s.accept()
    print 'NEW connection with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(client_thread, (conn,))

s.close()
