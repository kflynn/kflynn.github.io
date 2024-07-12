from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL and extract the query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # # Log the query parameters
        # print(f"GET {parsed_url.path} (params {query_params}")

        # Serve the local file
        try:
            with open("." + parsed_url.path, "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                body = file.read().decode()

                # Replace the query parameters in the file
                for key, value in query_params.items():
                    body = body.replace(f"{{{key}}}", value[0])

                self.wfile.write(body.encode())
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"File not found")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print("Server running on port", port)
    httpd.serve_forever()

run()