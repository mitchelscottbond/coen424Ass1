import socket
import numpy as np
import protoFile_pb2
from google.protobuf import text_format
import os

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

proto = protoFile_pb2.RFW() 
proto.RFWID = RFWID
proto.benchmarkType = benchMarkType
proto.workloadMetric = workloadMetric
proto.batchUnit = batchunit
proto.batchID = batchid
proto.batchSize = batchsize
proto.dataType = data_type
proto.dataAnalytics = analytics

path1 = os.getcwd()
filepath1 = path1 + '\ProtoBuff_Messages\RFW_proto.txt'
with open(filepath1, 'w') as outfile1:
    
    text_format.PrintMessage(proto, outfile1)


HOST = "localhost"  # The server's hostname or IP address
PORT = 50000  # The port used by the server
# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    print(proto)
    msg = proto.SerializeToString()
    print(msg)
    sock.send(msg)

    # Receive data from the server and shut down
    received = sock.recv(1000000000)
    protoResponse = protoFile_pb2.RFD()
    response = protoResponse.FromString(received)

finally:
    sock.close()
print(f"Received {response!r}")

path2 = os.getcwd()
filepath2 = path2 + '\ProtoBuff_Messages\RFD_proto.txt'
with open(filepath2, 'w') as outfile2:
    
    text_format.PrintMessage(response, outfile2)
