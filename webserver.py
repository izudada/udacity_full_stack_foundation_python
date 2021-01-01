from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = b"<html> <body> Hello! <br> <br> <a href='/holla'> Go to Holla</a> <br>"
                output += b"<form method='POST' enctype='multipart/form-data' action=='/hello'> <h2>What would you like to say? </h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form> "
                output += b"</body> </html>"
                self.wfile.write(output)
                print(output)
                return

            elif self.path.endswith("/holla"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = b"<html> <body> &#161Holla! <br> <br> <a href='/hello'> Back to Hello</a> <br> "
                output += b"<form method='POST' enctype='multipart/form-data' action=='/hello'> <h2>What would you like to say? </h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form> "
                output += b"</body> </html>"
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404, f"file not found {self.path}")
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get_content_charset('content-type'))
            messagecontent = {}
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            
            output = b""
            output += b"<html><body>"
            output += b" <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += b'''<form method='POST' enctype='multipart/form-data' action='hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += b"</body></html>"
            self.wfile.write(output)
            print(output)
        except Exception as e:
            print(e)

def main():
    try:
        port  = 8080
        server = HTTPServer(('', port), webserverHandler)
        print(f"Web server is running on port {port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("C entered... Shutting down server...")
        server.socket.close()

if __name__ == '__main__':
    main()