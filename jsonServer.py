import socket
import json
import csv
import numpy as np
import os

#encode via latin-1
HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

#Creating sockets and listening on port 50000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            #Receiving data over connection
            data = conn.recv(1000000000)
            jsonstring = data.decode('latin-1')
            
            #loading the decoded message into a json object and checking errors.
            try:
                jsonobj = json.loads(jsonstring)
            except:
                print('cant fix this error even if the json loads perfectly normally')
            

            ##getting all my data from the RFW.
            RFWID = jsonobj['RFWID']
            benchmark_type = jsonobj['benchmarkType']
            workload_metric = jsonobj['workloadMetric']
            batch_unit = jsonobj['batchUnit']
            batch_ID = jsonobj['batchID']
            batch_size = jsonobj['batchSize']
            data_type = jsonobj['dataType']
            data_analytics = jsonobj['dataAnalytics']

            #Creating the filename and checking which column to receive the data from.         
            filename = benchmark_type + '-' + data_type + '.csv'
            def check_workload_metric(workload_metric):
                if workload_metric == "CPU":
                    workload_column = 0
                elif workload_metric == "NetworkIn":
                    workload_column = 1 
                elif workload_metric == "NetworkOut":
                    workload_column = 2
                elif workload_metric == "Memory":
                    workload_column = 3
                return workload_column

            workload_column = check_workload_metric(workload_metric)

            #calculating batch size as well as specific units to determine first and last element in batch
            required_return_amount= batch_unit * batch_size
            first_element_in_batch = batch_unit*(batch_ID-1) 
            last_element_in_batch = first_element_in_batch + required_return_amount
            last_batch_ID = batch_size + (batch_ID-1)

            #Reading from the CSV files and storing them into a list.
            def retrieve_data_to_spec(filename, first_element_in_batch, last_element_in_batch, workload_column):
                with open(filename) as csv_file:
                    #prepping a list to be used later
                    my_returnable_list = []
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    allRows = list(csv_reader)
                    interestedRows = allRows[first_element_in_batch+1:last_element_in_batch+1]

                    for row in interestedRows:
                        my_returnable_list.append(row[workload_column])
                        line_count+=1

                #ensuring data is not type string but type int or float etc...
                res = [eval(i) for i in my_returnable_list]
                return res

            data_list = retrieve_data_to_spec(filename, first_element_in_batch, last_element_in_batch, workload_column)
            
            #sorting the list of data to perform my analytics
            sorted_data_list = sorted(data_list)

            #Using numpy to perform the data anlytics
            def perform_data_analytics(data_list, data_analytics):
                a= np.array(data_list)

                if data_analytics == "avg":
                    p = np.average(a)

                elif data_analytics == "std":
                    p = np.std(a)

                elif data_analytics == "max":
                    p = np.max(a)

                elif data_analytics =="min":
                    p = np.min(a)

                else:
                    temp = int(data_analytics.replace('p', ''))
                    p = np.percentile(a, temp)

                return p

            analytics = perform_data_analytics(sorted_data_list, data_analytics)

            RFDmessage = {}
            RFDmessage["RFWID"]=RFWID
            RFDmessage["lastBatchID"]= last_batch_ID
            RFDmessage["dataSamples"] =data_list
            analytics = str(analytics)
            RFDmessage["dataAnalytics"]=analytics

            response = json.dumps(RFDmessage)

            if not data:
                break

            conn.send(response.encode('latin-1'))