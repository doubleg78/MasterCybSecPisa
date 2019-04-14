import socket
import sys
from thread import *

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
    data = conn.recv(1024)
    if data.split('|')[0] == 'REGISTER':
        # msg format: REGISTER|USER|IP|PORT
        print data
        result = adduser(data.split('|')[1], data.split('|')[2], data.split('|')[3])
        if result == 'ADDED USER':
            conn.send('OK')
        if result == 'ERROR':
            conn.send('Nickname already present')
        conn.close()
        for i, d in enumerate(user_table):
            line = '|'.join(str(x).ljust(22) for x in d)
            print(line)
            if i == 0:
                print('-' * len(line))
    conn.close()


def adduser(cNick, cHost, cPort):
    for x, data in enumerate(user_table):
        if data[0] == cNick:
            #del user_table[x]
            print('ERROR: User already registered...checking if still alive')
            ## inserire codice per verificare se online
            ## se online ritorna error altrimenti cancella e aggiunge utente
            return 'ERROR'
    user_table.append([cNick, cHost, cPort])
    return 'ADDED USER'


while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread, (conn,))

s.close()
