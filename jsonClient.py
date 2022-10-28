import socket
import sys
import json
import csv
import numpy as np

benchmarkType = ""
workloadMetric = ""
global batchunit
global batchid
global batchsize
data_type = ""
print('Enter the RFW ID:')
RFWID =  input()
print("Enter bench mark type: 1 for 'DVD' or enter 2 for 'NDBench' for bench mark type")
while True:
    benchmarktemp = input()
    if benchmarktemp == "1":
        benchMarkType = "DVD"
        break
    elif benchmarktemp =="2":
        benchMarkType = "NDBench"
        break
    else:
        print("Invalid input for bench mark type, try again:")


print("Enter Workload Metric: '1 for = CPUUtilization_Average' '2 = NetworkIn_Average' '3 = NetworkOut_Average' '4 = MemoryUtilization_Average'")
while True:
    workloadmet = input()
    if workloadmet == "1":
        workloadMetric ="CPU"
        break
    elif workloadmet == "2":
        workloadMetric ="NetworkIn"
        break
    elif workloadmet == "3":
        workloadMetric = "NetworkOut"
        break
    elif workloadmet == "4":
        workloadMetric = "Memory"
        break
    else:
        print("Invalid input for workload metric, try again:")


print("Enter batch unit as an integer")

while True:
    batchun = input()
    batchunit = int(batchun)
    if type(batchunit) == int:
        break
    else:
        print("Invalid input for batch unit, try again:")


print("Enter batch ID as an integer")
while True:
    temp = input()
    batchid = int(temp)
    if type(batchid) == int:
        break
    else:
        print("Invalid input for batch unit, try again:")

print("Enter batch size as an integer")
while True:
    temp = input()
    batchsize = int(temp)
    if type(batchsize) == int:
        break
    else:
        print("Invalid input for batch unit, try again:")


print("Enter data type: '1 = testing' '2 = training'")

while True:
    datatype = input()
    if datatype == "1":
        data_type="testing"
        break
    elif datatype == "2":
        data_type ="training"
        break
    else:
        print("Invalid input for workload metric, try again:")

print("Enter data analytics in the format of '99p', or '50p', or '10p', or '70p', or 'avg', or 'std', or 'max', or 'min'\n If one of these values are not entered, the code will not function correctly")
analytics = input()



RFWmessage = {}
RFWmessage["RFWID"]=RFWID
RFWmessage["benchmarkType"]= benchMarkType
RFWmessage["workloadMetric"] = workloadMetric
RFWmessage["batchUnit"] = batchunit
RFWmessage["batchID"] = batchid
RFWmessage["batchSize"] = batchsize
RFWmessage["dataType"] = data_type
RFWmessage["dataAnalytics"]=analytics
request = json.dumps(RFWmessage)

data_temp = json.dumps(request)
HOST = "localhost"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

#Code for if I want to open rfw.json and use it. 
    #f=  open('RFW.json')
    #m= json.load(f)
    #data =json.dumps(m)
print(data_temp)
data_temp2 = data_temp.replace("\\", "")
data = data_temp2.lstrip('"').rstrip('"')
print(data)

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