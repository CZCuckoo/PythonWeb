from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

#sets variable form with all of the html data necessary for the form.
form = '''<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST" action="http://localhost:8000/">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
'''

class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        #Determine how long the message is
        length = int(self.headers.get('Content-length', 0))

        #Read the correct amount of data
        data = self.rfile.read(length).decode()

        #Extract the data from the message
        message = parse_qs(data)["message"][0]

        #Send the message back as a response
        #Send response 200 to let server know it's good
        self.send_response(200)

        #send header info
        self.send_header('Content-type', 'text/plain; charset=utf-8')

        #send blank line to end header info
        self.end_headers()

        #take variable message, and write it
        self.wfile.write(message.encode())

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset="utf-8')
        self.end_headers()

        #Take form info, as written in the variable above, and send it as html
        self.wfile.write(form.encode())



if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
