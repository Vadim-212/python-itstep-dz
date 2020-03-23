import socketserver
import xmltodict
import json
import xml.parsers.expat


HOSTNAME = 'localhost'
PORT = 8182


class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        print(f'connection received: {self.client_address}')
        data = self.rfile.readline().strip()
        print(f'data received: {data.decode()}')
        
        try:
            my_dict=xmltodict.parse(data.decode())
            json_data=json.dumps(my_dict)
            print(json_data)
        except xml.parsers.expat.ExpatError:
            print('Wrong XML!')
            self.wfile.write(b'Error: wrong XML!')
            return
        
        #self.wfile.write(data.upper())
        self.wfile.write(json_data.encode())


if __name__ == "__main__":

    with socketserver.TCPServer((HOSTNAME, PORT), MyTCPHandler) as server:
        server.serve_forever()
