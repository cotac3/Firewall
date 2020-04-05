# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 16:42:34 2020

@author: cotac
"""

import socket
import threading

def main():
    #host set to localhost
    host = ''
    #port number (with no collisions) to listen on
    port = 30001
    #creates a TCP socket
    server_socket = socket.socket()
    #binds socket to address and port
    server_socket.bind((host,port))
    #Can handle up to 100 connections at a time (may be increased or decreased)
    server_socket.listen(100)
    #forever will accept new TCP connections
    while True:
        #accepts the connection
        #conn = sets newly created socket
        #address = address and the port of the client 
        conn, address = server_socket.accept()
        #Creating a new thread and passing the socket and address 
        t = threading.Thread(target = handler, args = (conn, address))
        #starts the thread 
        t.start()
    return 0
 #recieves the first packet
def handler(server_socket, address):
    #sets number of bytes able to be recieved 
    data = server_socket.recv(8192)
     #if no data, then returned
    if len(data) == 0: 
        return
    
    # split packet by line
    lines = data.split(b"\r\n")
    
    # split lines[1] by space, into an array
    lines = lines[1].split(b" ")
    
    # url and port from the array
    urlAndPort = lines[1]

    # separate port and url
    lines = urlAndPort.split(b":")
    
    # run if urlAndPort is something like "go.com:80"
    if len(lines) > 1:
        url = lines[0].decode()
        port = int(lines[1])
        
    # run if urlAndPort is something like "go.com"
    else:
        url = urlAndPort.decode()
        port = 80
        
    #website blocking 
    if url == "go.com":
        print("Website Blocked!")
        server_socket.close()
        return
    #printing out thr URl and port for the first packet 
    print("URL: " + url)
    print("Port: " + str(port))
    print("-------------------")
    
    #client
    #create a new TCP connection with the webserver 
    client_socket = socket.socket()
    # Actually connects the webserver
    client_socket.connect((url, port))
    # Sends the first packet to the webserver, var data is recieved from the browser then sent to the webserver
    client_socket.send(data)
    
    try:
        #Keep recieveing packets from the webserver forever 
        while True:
            # read response from actual web server
            data = client_socket.recv(8192)
            
            # if data is not empty
            if len(data) > 0:
                # send it back to browser
                server_socket.send(data)
                
            # otherwise, leave loop
            else:
                break
            
        #closing connecting to client broser and the webserver once done 
        client_socket.close()
        server_socket.close()
    #If an error occurs, we close connecting to the browser client and the webserver 
    except Exception as e:
        client_socket.close()
        server_socket.close()
        
if __name__== '__main__':
    main()