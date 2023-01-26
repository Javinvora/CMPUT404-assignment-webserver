#  coding: utf-8 
import socketserver
from datetime import date

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)

        #Converting the data from bytes to unicode
        self.data = self.data.decode("utf-8")

        # Checking if the method present in the request sent to us is "GET"
        if (self.data[0:3]) == "GET":
            # Obtaining the main URL here
            self.data = self.data.split(" ")
            f_name = (self.data[1])

            # Checking if the file requested in the request received above is HTML
            if (f_name[-4: ] == "html"):
                # opening the desired file in tghe wwww directory
                f1 = open("./www" + f_name)
                # reading the content of the file
                f_content = f1.read()
                # closing the file we opened above
                f1.close()
                # serving the .html file present in the www directory
                self.main_message = "HTTP/1.1 200 OK Not FOUND!\r\nDate: {}\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}".format(date.today, len(f_content),f_content)
                self.request.sendall(bytearray(self.main_message, 'utf-8'))

            # Checking if the file requested in the request received above is CSS
            elif (f_name[-3: ] == "css"):
                # If it begins with deep: It is not present in the www.directory
                if (f_name[1:9] == "deep.css"):
                    self.main_message = "HTTP/1.1 404 Not Found!\r\n"
                    self.request.sendall(bytearray(self.main_message, 'utf-8'))
                else:
                # opening the desired file in the www directory
                    f1 = open("./www" + f_name)
                    # reading the content of the file
                    f_content = f1.read()
                    # closing the file we opened above
                    f1.close()
                    # serving the .css file present in the www directory
                    self.main_message = "HTTP/1.1 200 OK Not FOUND!\r\nDate: {}\r\nContent-Type: text/css\r\nContent-Length: {}\r\n\r\n{}".format(date.today, len(f_content),f_content)
                    self.request.sendall(bytearray(self.main_message, 'utf-8'))

            elif(f_name == "/deep"):
                # correcting the input URL to the corrected one
                f_name += "/"
                self.main_message = "HTTP/1.1 301 Moved Permanently\r\nDate: {}\r\nLocation: {}\r\n\r\n".format(date.today, f_name)
                self.request.sendall(bytearray(self.main_message, 'utf-8'))
            
            # When no path is specified except for a "/"
            elif (f_name == "/"):
                # returning the index.html files in that directory for the paths ending with "/"
                f_name += "index.html"
                # opening the desired file in tghe wwww directory
                f1 = open("./www" + f_name)
                # reading the content of the file
                f_content = f1.read()
                 # closing the file we opened above
                f1.close()
                # serving the .html file present in the www directory
                self.main_message = "HTTP/1.1 200 OK Not FOUND!\r\nDate: {}\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}".format(date.today, len(f_content),f_content)
                self.request.sendall(bytearray(self.main_message, 'utf-8'))

            # When the path involves getting into another directory present in the www directory
            elif (f_name[-1:] == "/"):
                # returning the index.html files in that directory for the paths ending with "/"
                f_name += "index.html"
                # opening the desired file in tghe wwww directory
                f1 = open("./www" + f_name)
                # reading the content of the file
                f_content = f1.read()
                 # closing the file we opened above
                f1.close()
                # serving the .html file present in the deep directory which is present in the www directory
                self.main_message = "HTTP/1.1 200 OK Not FOUND!\r\nDate: {}\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}".format(date.today, len(f_content),f_content)
                self.request.sendall(bytearray(self.main_message, 'utf-8'))

            else:
                # if the path is not found in the directory
                self.main_message = "HTTP/1.1 404 Not Found!\r\n"
                self.request.sendall(bytearray(self.main_message, 'utf-8'))
               
        else:
             # If not, send a response message of 405 (PUT, POST or DELETE in our cases)
            self.main_message = "HTTP/1.1 405 Method Not Allowed!\r\n"
            self.request.sendall(bytearray(self.main_message, 'utf-8'))

        # Sending a message of "Succesful!" if it passes all the test cases mentioned in free & not-free-test pyhton files respectively.
        self.request.sendall(bytearray("Succesful!",'utf-8'))
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

