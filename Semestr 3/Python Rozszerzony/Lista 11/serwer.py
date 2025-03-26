from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class MyHttpHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><head><title>test</title></head>')
        self.wfile.write(b'<body>')
        if self.path == '/uptime': self.uptime()
        else: self.menu()
        self.wfile.write(b'</body></html>')

    def uptime(self):
        res = bytes(os.popen("uptime").read(),'utf-8')
        self.wfile.write(b'<h1>Rezultat</h1>')
        self.wfile.write(b'<tt>' + res + b'</tt>')

    def menu(self):
        self.wfile.write(b'<h1>Serwer</h1>')
        self.wfile.write(b'<ul>')
        self.wfile.write(b'<li><a href="uptime">uptime</a></li>')
        self.wfile.write(b'</ul>')



address = ('', 8000)
httpd = HTTPServer(address, MyHttpHandler)
httpd.serve_forever()