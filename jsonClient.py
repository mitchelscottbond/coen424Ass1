import socket
import json
import numpy as np
import os

#Global variables for my RFW
benchmarkType = ""
workloadMetric = ""
global batchunit
global batchid
global batchsize
data_type = ""

#Performing checks on user inputs for the RFW
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


#Creating my Request for workload dictionary.
RFWmessage = {}
RFWmessage["RFWID"]=RFWID
RFWmessage["benchmarkType"]= benchMarkType
RFWmessage["workloadMetric"] = workloadMetric
RFWmessage["batchUnit"] = batchunit
RFWmessage["batchID"] = batchid
RFWmessage["batchSize"] = batchsize
RFWmessage["dataType"] = data_type
RFWmessage["dataAnalytics"]=analytics

path = os.getcwd()
filepath = path + '\RFW_RFD_Messages\RFW.json'
with open(filepath, 'w') as outfile1:
    
    json.dump(RFWmessage, outfile1, indent = 6)

request = json.dumps(RFWmessage)

data_temp = json.dumps(request)
HOST = "localhost"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

#Stripping unnecssary blackslashes and quotations that are not needed. 
data_temp2 = data_temp.replace("\\", "")
data = data_temp2.lstrip('"').rstrip('"')


# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    print('This is the RFW below:')
    print(data)
    sock.send(data.encode('latin-1'))


    # Receive data from the server and shut down
    received = sock.recv(1000000000)
    received = received.decode('latin-1')

finally:
    sock.close()

print('This is the RFD received below:')
print(f"Received {received!r}")
jsonobj = json.loads(received)

path2 = os.getcwd()
filepath2 = path2 + '\RFW_RFD_Messages\RFD.json'
with open(filepath2, 'w') as outfile2:
    
    json.dump(jsonobj, outfile2, indent = 6)


