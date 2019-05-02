# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:47:05 2017

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

# SSLContext to accept clients' connections with client authentication:
sslContext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslContext.load_verify_locations("ca_cert.pem")
sslContext.load_cert_chain("server_cert.pem", "server_prvkey.pem")
sslContext.verify_mode = ssl.CERT_REQUIRED

wrappedSocket = sslContext.wrap_socket(s, server_side=True)

# Dopo aver creato il socket, questo deve essere
# assegnato un indirizzo IP e una porta sulla 
# quale si mettera’ in ascolto (il sistema operativo inoltrera’ 
# tutti i messaggi destinati a quella porta al socket in questione)
try:
    # Il primo argomento e’ l’indirizzo IP (tra 
    # quelli assegnati all’host) sulla quale mettersi in ascolto
    # Una stringa vuota sta a significare che il socket verra’ messo in 
    # asclto su tutti gli indirizzi disponibili sull’host
    # Il secondo argomento e’ la porta
    wrappedSocket.bind(('', 8888))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Mette in ascolto il socket
# L’argomento indica il numero massimo di 
# richieste che possono essere messe in coda 
# prima di essere gestite
wrappedSocket.listen(10)
print 'Socket now listening'

# Mettersi in attesa e accettare connessioni in 
# ingresso – funzione bloccante
conn, addr = wrappedSocket.accept()
# Quando una connessione viene accettata la 
# funzione si sblocca
# Questa ritorna un nuovo socket (conn) che e’ 
# destinato unicamente per la comunicazione con quel 
# client e una struttura che contiene informazioni 
# sul client che si e’ appena connesso
print 'Connected with ' + addr[0] + ':' + str(addr[1])
print 'Client certificate:', conn.getpeercert()

# Il nuovo socket puo’ essere usato per 
# ricevere/inviare dati da/verso il client che 
# si e’ connesso
data = conn.recv(1024)
# In questo caso di replica con gli stessi dati 
# inviati dal client con l’aggiunta di un prefisso
reply = 'OK...' + data    
conn.sendall(reply)
# e alla fine si chiudono tutte le connessioni
conn.close()
wrappedSocket.close()


