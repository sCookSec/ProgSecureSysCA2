from http.server import HTTPServer, BaseHTTPRequestHandler
import database
import router

# Init database
database.init_database()

# Set server address
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# Create a custom request handler class
class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    # Pass all GET requests to our router
    def do_GET(self):
        router.handle_request('get', self)
    
    # Pass all POST requests to our router
    def do_POST(self):
        router.handle_request('post', self)

# Create HTTPServer
httpd = HTTPServer((SERVER_HOST, SERVER_PORT), CustomHTTPRequestHandler)

# Init HTTPServer
print(f"Web server listening in port {SERVER_PORT}...")
httpd.serve_forever()