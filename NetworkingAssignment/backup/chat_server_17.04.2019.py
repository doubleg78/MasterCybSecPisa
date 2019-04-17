import socket
import sys
from thread import *
import asciiart

#HOST = str(sys.argv[1])
#PORT = str(sys.argv[2])
HOST = '127.0.0.1'
PORT = 8888

user_table = [['NiCkNaMe', 'IP', 'PORT']]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'DEBUG: Socket created'

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'DEBUG: Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'DEBUG: Socket bind complete'

# Start listening on socket
s.listen(100)
print 'DEBUG: Socket now listening'


def clientthread(conn):
    def show_users():
        for i, d in enumerate(user_table):
            line = '|'.join(str(x).ljust(22) for x in d)
            print(line)
            if i == 0:
                print('-' * len(line))

    data = conn.recv(1024)

    if data.split('|')[0] == 'REGISTER':
        # msg format: REGISTER|USER|IP|PORT
        print data
        client_request = data.split('|')
        # result = adduser(data.split('|')[1], data.split('|')[2], data.split('|')[3])
        result = adduser(client_request[1], client_request[2], client_request[3])
        if result == 'ADDED USER':
            conn.send('OK')
        if result == 'ERROR':
            conn.send('Nickname already present')
        conn.close()
        show_users()

    if data.split('|')[0] == 'DEREGISTER':
        # msg format: DEREGISTER|USER
        print data
        client_request = data.split('|')
#        for x, users in enumerate(user_table):
#            if users[0] == client_request[1]:
#                del user_table[x]
        if del_user(client_request[1]) == 'OK':
            print client_request[1] + ' User DeRegistered Successfully'
            show_users()

    if data.split('|')[0] == 'SEARCH':
        # msg format: SEARCH|USER
        print data
        client_response = ''
        client_request = data.split('|')
        for x, users in enumerate(user_table):
            if users[0] == client_request[1]:
                if check_user_online(users[1], int(users[2])) == 'USER_ONLINE':
                    client_response = ('USERINFO|' + users[1] + '|' + users[2])
                    break
                else:
                    del_user(client_request[1])
                    client_response = 'ERROR'
                    break
        if client_response == '':
            client_response = 'ERROR'
        conn.sendall(client_response)

    if data.split('|')[0] == 'USERS':
        # msg format: USERS|
        print data
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
            print('ERROR: User already registered...checking if still alive')

            check = check_user_online(data[1], int(data[2]))

            if check == 'USER_OFFLINE':
                print('USER Offline, deleting and registering new data')
                del user_table[x]
            else:
                print('USER Online and registered with the server')
                return 'ERROR'
    user_table.append([cNick, cHost, cPort])
    return 'ADDED USER'


def check_user_online(UDP_IP, UDP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto('PING?PONG', (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024)
        print "received message:", data
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
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread, (conn,))

s.close()
