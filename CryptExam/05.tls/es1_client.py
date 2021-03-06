# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:29:24 2017

@author: Pericle
"""

import socket   #for sockets
import sys  #for exit
import ssl  #for TLS
  
try:
    # Crea uno STREAM socket (TCP/IP) 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()
    

# SSLContext for connecting to https://www.google.com:
sslContext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)

wrappedSocket = sslContext.wrap_socket(s, server_side=False, server_hostname='google.com')

# Primo argomento IP Address dell’host remoto
# Numero Porta associata al processo server

host = "172.217.23.78"
port = 443
wrappedSocket.connect((host, port))

print 'Socket Connected'
print 'Cipher:', wrappedSocket.cipher()

# Dati da inviare
message = "GET / HTTP/1.1\r\n\r\n"

try:
    # Invio i dati
    wrappedSocket.sendall(message)
except socket.error:
    # L’invio e’ fallito
    print 'Send failed'
    sys.exit()

print 'Send successful'

# Ricevere i dati (l’argomento della funzione e’ 
# il numero massimo dei dati che puo’ essere 
# ricevuto). Il ritorno della funzione recv e’ una 
# stringa che rappresenta i dati ricevuti
reply = wrappedSocket.recv(4096)
# Stampa il messaggio ricevuto
print reply

# Chiudere il socket
wrappedSocket.close()
