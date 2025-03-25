import socketserver
import argparse

import http.server

DEFAULT_PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with additional features."""
    
    def do_GET(self):
        # Example of custom path handling
        if self.path == '/hello':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Send message
            message = "<html><body><h1>Hello, World!</h1></body></html>"
            self.wfile.write(bytes(message, "utf8"))
            return
        
        # Default behavior for other paths
        return super().do_GET()

def run_server(port, use_custom_handler=False):
    """Run the HTTP server on the specified port."""
    
    handler = CustomHTTPRequestHandler if use_custom_handler else http.server.SimpleHTTPRequestHandler
    
    # Create server
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server started at http://localhost:{port}")
        # Keep the server running
        httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a simple HTTP server')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                        help=f'Port to run the server on (default: {DEFAULT_PORT})')
    parser.add_argument('--custom', action='store_true',
                        help='Use custom request handler with additional features')
    
    args = parser.parse_args()
    
    try:
        run_server(args.port, args.custom)
    except KeyboardInterrupt:
        print("\nShutting down the server...")