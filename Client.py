import socket
import sys
import json
import csv
import numpy as np
















HOST = "localhost"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect((HOST, PORT))
#    s.sendall(b"Hello, world")
#    data = s.recv(1024)

#print(f"Received {data!r}")

#m ='{"id": 2, "name": "abc"}'
#m = {"RFWID":'123',"benchmarkType":'DVD',"workloadMetric":'CPU',"batchUnit":10,"BatchID":2,"batchSize":9,"dataType":'testing',"dataAnalytics":'99p'} # a real dict.

#data = json.dumps(m)
f=  open('RFW.json')
m= json.load(f)
data =json.dumps(m)

#temp = data[0]
print("this is my temp variable")
#print(temp)

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    print(data)
    sock.send(data.encode('latin-1'))


    # Receive data from the server and shut down
    received = sock.recv(1000000000)
    received = received.decode('latin-1')

finally:
    sock.close()
print(f"Received {received!r}")

#print "Sent:     {}".format(data)
#print "Received: {}".format(received)