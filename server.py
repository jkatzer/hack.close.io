import os
import SimpleHTTPServer
import SocketServer

os.chdir('.generated')
PORT = 8080 
HOSTNAME = "localhost"

httpd = SocketServer.TCPServer((HOSTNAME, PORT), 
                                SimpleHTTPServer.SimpleHTTPRequestHandler)

print("serving on http://%s:%d" % (HOSTNAME, PORT))
httpd.serve_forever()

