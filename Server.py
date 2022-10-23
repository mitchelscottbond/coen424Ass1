import socket
import urllib


print("Creating TCP socket")

#Creates TCP socket.
serversocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to specific port on localhost.
server_address = ('localhost', 12000)
print("starting the tcp socket on port 12000")
serversocket1.bind(server_address)


while True:
    #listen for incoming connections on your socket
    serversocket1.listen(1)
    print("waiting for a connection")

    #socket.accept() method accepts an incoming socket request. 
    connection, client_address = serversocket1.accept()
    req = connection.recv(2048).decode()
    print(req) # prints the incoming HTTP request for parsing.

    #Parses the request to get the correct portion of the file
    parsedReq = req.split('GET /')
    newParsedReq = parsedReq[1].split(' ')
    filename = newParsedReq[0] + ".html"
    print(filename)

    if filename != "coen366.html":
        header = 'HTTP/1.1 200 OK\nContent-Type: text/html \n\n'
        message =  '<html><body><h1>Page Not Found</h1></body></html>'.encode('utf-8')
    else: 
        file = open(filename, 'rb')
        message = file.read()
        file.close()
        header = 'HTTP/1.1 200 OK\nContent-Type: text/html \n\n'

    finalHeader = header.encode('utf-8')    
    finalResponse = finalHeader + message

    connection.send(finalResponse)
    connection.close()