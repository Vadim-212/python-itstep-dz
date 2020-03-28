import socketserver
import xmltodict
import dicttoxml
import json
import xml.parsers.expat

import ast


HOSTNAME = 'localhost'
PORT = 8182


class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        print(f'connection received: {self.client_address}')
        data = self.rfile.readline().strip()
        print(f'data received: {data.decode()}')
        
        try:
            my_dict=xmltodict.parse(data.decode())
            data=json.dumps(my_dict)
            print(data)
        except xml.parsers.expat.ExpatError: 
            try:
                my_dict = ast.literal_eval(data.decode())
                data=dicttoxml.dicttoxml(my_dict)
                print(data) 
            except:
                print('Wrong data!')  
                self.wfile.write(b'Error: wrong data!')
                return
        try:
            self.wfile.write(data.encode())
        except AttributeError:
            self.wfile.write(data)


if __name__ == "__main__":

    with socketserver.TCPServer((HOSTNAME, PORT), MyTCPHandler) as server:
        server.serve_forever()
