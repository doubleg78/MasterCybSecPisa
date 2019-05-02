import SocketServer
import socket
import threading
import time

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        
        self.request.send("OK" + data)
        return


    
address = ('', 8888)
server = SocketServer.TCPServer(address, EchoRequestHandler)
ip, port = server.server_address # find out what port we were given
   
t = threading.Thread(target=server.serve_forever)
t.setDaemon(True)
t.start()

time.sleep(300)

server.shutdown()


