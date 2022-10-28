import socket
import csv
import numpy as np
import protoFile_pb2
import json

#encode via latin-1
HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 50000  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1000000000)
            print(data)

            protoData = protoFile_pb2.RFW()
            msg = protoData.FromString(data)

            ##getting all my data from the RFW.
            RFWID = msg.RFWID
            benchmark_type = msg.benchmarkType
            workload_metric = msg.workloadMetric
            batch_unit = msg.batchUnit
            batch_ID = msg.batchID
            batch_size = msg.batchSize
            data_type = msg.dataType
            data_analytics = msg.dataAnalytics
            
            #If benchmark_type is null, all the following code will crash so I close the script before the code crashes if that happens. 
            if benchmark_type =="":
                exit()
            
            filename = benchmark_type + '-' + data_type + '.csv'
            def check_workload_metric(workload_metric):
                if workload_metric == "CPU":
                    workload_colum = 0
                elif workload_metric == "NetworkIn":
                    workload_colum = 1 
                elif workload_metric == "NetworkOut":
                    workload_colum = 2
                elif workload_metric == "Memory":
                    workload_colum = 3
                elif workload_metric == "":
                    workload_colum = 0
                return workload_colum

            workload_column = check_workload_metric(workload_metric)

            #calculating batch size as well as specific units to determine first and last element in batch
            required_return_amount= batch_unit * batch_size
            first_element_in_batch = batch_unit*(batch_ID-1) 
            last_element_in_batch = first_element_in_batch + required_return_amount
            last_batch_ID = batch_size + (batch_ID-1)

            #
            def retrieve_data_to_spec(filename, first_element_in_batch, last_element_in_batch, workload_column):
                with open(filename) as csv_file:
                    #prepping a list to be used later
                    my_returnable_list = []
                    #heading = next(csv_file)
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    allRows = list(csv_reader)
                    interestedRows = allRows[first_element_in_batch+1:last_element_in_batch+1]

                    for row in interestedRows:
                        my_returnable_list.append(row[workload_column])
                        line_count+=1
                
                    #print("my list of data points is given below. It can be modified to print by new lines or in the format it is currentyl shown by changing the backslah t to a backslah n")
                    #print(*my_returnable_list, sep = "\t")
                    #print(f'Processed {line_count} lines.')

                #ensuring data is not type string but type int or float etc...
                res = [eval(i) for i in my_returnable_list]
                print("List of data as it's data type is: ", res)

                
                return res

            data_list = retrieve_data_to_spec(filename, first_element_in_batch, last_element_in_batch, workload_column)
            sorted_data_list = sorted(data_list)
            def perform_data_analytics(data_list, data_analytics):
                a= np.array(data_list)
                print("printing numpy array in ascending order")
                print(*a)

                if data_analytics == "avg":
                    p = np.average(a)
                    print("average = ")
                    print(p)
                elif data_analytics == "std":
                    p = np.std(a)
                    print("std = ")
                    print(p)
                elif data_analytics == "max":
                    p = np.max(a)
                    print("max = ")
                    print(p)
                elif data_analytics =="min":
                    p = np.min(a)
                    print("min = ")
                    print(p)
                else:
                    temp = int(data_analytics.replace('p', ''))
                    p = np.percentile(a, temp)
                    print('else percentile = ')
                    print( p)
                return p

            analytics = perform_data_analytics(sorted_data_list, data_analytics)
            print('results of data analytics')
            print(analytics)

            RFDmessage = {}
            RFDmessage["RFWID"]=RFWID
            RFDmessage["lastBatchID"]= last_batch_ID
            RFDmessage["dataSamples"] =data_list
            RFDmessage["dataAnalytics"]=analytics

            proto = protoFile_pb2.RFD() 
            proto.RFWID = RFWID
            proto.LastBatchID = last_batch_ID
            proto.dataRequested.extend(data_list)
            proto.dataAnalytics = analytics

            response = proto.SerializeToString()

            if not data:
                break
                
            conn.send(response)