from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
import socket  # for sockets
import sys  # for exit
import ssl  # for TLS

SHARED_PASS = '1234'

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

# SSLContext for connecting to Server:
sslContext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
sslContext.load_verify_locations("CA_Certs//GG Company CA_cert.pem")
sslContext.check_hostname = False
wrappedSocket = sslContext.wrap_socket(s, server_side=False)

host = "127.0.0.1"
port = 8888
wrappedSocket.connect((host, port))

print 'Socket Connected'
print 'Cipher:', wrappedSocket.cipher()

challenge = wrappedSocket.recv(4096)
print challenge

ctx = hmac.HMAC(SHARED_PASS, hashes.SHA256(), default_backend())
ctx.update(challenge)
digest = ctx.finalize()

try:
    # Invio i dati
    wrappedSocket.sendall(digest)
except socket.error:
    print 'Send failed'
    sys.exit()

# Chiudere il socket
wrappedSocket.close()
