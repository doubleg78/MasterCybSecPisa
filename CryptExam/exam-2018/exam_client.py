# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:32:32 2017

@author: Pericle
"""

import socket   #for sockets
import sys  #for exit
import ssl  #for TLS
from cryptography.hazmat.primitives import hashes, hmac   #for HMAC
from cryptography.hazmat.backends import default_backend  #for HMAC backend

password = "pSsW"

try:
    # Crea uno STREAM socket (TCP/IP) 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()
    

# SSLContext for connecting to Server:
sslContext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
sslContext.load_verify_locations("ca_cert.pem")

wrappedSocket = sslContext.wrap_socket(s, server_side=False, server_hostname='Server')

# Primo argomento IP Address dell’host remoto
# Numero Porta associata al processo server

host = "127.0.0.1"
port = 4444
wrappedSocket.connect((host, port))

print 'Socket Connected'
print 'Cipher:', wrappedSocket.cipher()

# Dati da inviare
message = "GET / HTTP/1.1\r\n\r\n"

# Receiving the challenge string:
challenge = wrappedSocket.recv(4096)

# Computing and sending the HMAC digest of the challenge string:
ctx = hmac.HMAC(password, hashes.SHA256(), default_backend())
ctx.update(challenge)
digest = ctx.finalize()

try:
    # Invio i dati
    wrappedSocket.sendall(digest)
except socket.error:
    # L’invio e’ fallito
    print 'Send failed'
    sys.exit()

print 'Send successful'

# Chiudere il socket
wrappedSocket.close()
