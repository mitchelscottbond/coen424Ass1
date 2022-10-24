import csv
import numpy as np



#Checking the file type that needs to be opened
benchmark_type = 'DVD'
data_type = 'testing'
filename = benchmark_type + '-' + data_type + '.csv'

#Checking column of data using the Workload Metric
workload_metric = "CPU"
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

#batch measurements
batch_ID = 2
batch_unit = 10
batch_size = 9

#calculating batch size as well as specific units to determine first and last element in batch
required_return_amount= batch_unit * batch_size
first_element_in_batch = batch_unit*(batch_ID-1) 
last_element_in_batch = first_element_in_batch + required_return_amount

#data statistics
data_analytics = "avg"
#testing printing the batch size
    #tons = list(range(1000))
    #my_list = tons[first_element_in_batch:last_element_in_batch]
    #print(*my_list, sep = ", ")



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

    sortedNewList = sorted(res)
    return sortedNewList

data_list = retrieve_data_to_spec(filename, first_element_in_batch, last_element_in_batch, workload_column)

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

result = perform_data_analytics(data_list, data_analytics)
print('results of data analytics')
print(result)






