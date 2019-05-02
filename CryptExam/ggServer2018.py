from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
import socket
import sys
import ssl
import os

SHARED_PASSWORD = '1234'

try:
    # Crea uno STREAM socket (TCP/IP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

# SSLContext to accept clients' connections:
sslContext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslContext.load_cert_chain("CA_Certs//GG_Server_cert.pem", "CA_Certs//GG_Server_key.pem")

wrappedSocket = sslContext.wrap_socket(s, server_side=True)

try:
    wrappedSocket.bind(('', 8888))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

wrappedSocket.listen(10)
print 'Socket now listening'

conn, addr = wrappedSocket.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

challenge = os.urandom(4)

conn.sendall(challenge)
data = conn.recv(1024)
print 'OK...' + data

ctx = hmac.HMAC(SHARED_PASSWORD, hashes.SHA256(), default_backend())
ctx.update(challenge)
try:
    ctx.verify(data)
except:
    print 'Digest not valid'

conn.close()
wrappedSocket.close()

