import os
import SimpleHTTPServer
import SocketServer

os.chdir('../public_html')
PORT = 8080 
HOSTNAME = "localhost"

class BlogHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        name, ext = os.path.splitext(path)
        if name.startswith('/posts/') and not ext:
            path += '.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)

SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer((HOSTNAME, PORT), BlogHandler)

print("serving on http://%s:%d" % (HOSTNAME, PORT))
httpd.serve_forever()

