import csv  
import os
import time
from datetime import datetime, timedelta
import itertools
import sys

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# my_file = os.path.join(THIS_FOLDER, 'example-input2.csv')
my_file = os.path.join(THIS_FOLDER, 'Fire_Department_Calls_for_Service.csv')


# define the name of the file to read from
filename = my_file

starttime = time.time()


def convertDateToYearMonthDay(date_string):
    # save date string into date object: current_row_date
    current_row_date = datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
    # convert date to string, only save year/month/day
    current_row_date = current_row_date.strftime('%Y/%m/%d')
    # convert from string back to datetime object
    current_row_date = datetime.strptime(current_row_date, '%Y/%m/%d')
    return current_row_date


def convertDateToYearMonth(date_string):
    # save date string into date object: current_row_date
    current_row_date = datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
    # convert date to string, only save year/month/day
    current_row_date = current_row_date.strftime('%Y/%m')
    # convert from string back to datetime object
    current_row_date = datetime.strptime(current_row_date, '%Y/%m')
    return current_row_date


def convertDateToHourMinuteSecond(date_string):
    # save date string into date object: current_row_date
    current_row_date = datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
    # # convert date to string, only save year/month/day
    # current_row_date = current_row_date.strftime('%H:%M:%S %p')
    # # convert from string back to datetime object
    # current_row_date = datetime.strptime(current_row_date, '%H:%M:%S %p')
    return current_row_date


def checkKey(dict, key):
    if key in dict:
        return True
    else:
        return False


def checkMonth(dict, key, month):
    if month in dict[key]:
        return True
    else:
        return False


def createResponseTimeArray():

    response_time_array = []

    with open(filename) as csvfile:  
        data = csv.DictReader(csvfile)
        for row in data:
            # example date string: 07/25/2019 07:18:15 PM

            # convert date to year/month/day
            current_row_date = convertDateToYearMonthDay(row['Received DtTm'])

            # create start and end date for desired date range
            date_start = datetime(2019, 1, 1)
            date_end = datetime(2020, 1, 1)

            # example dictionary entry
            # Dict['B01'] = {'2019-01': 504, '2019-02': 580}

            received_time = row['Received DtTm']
            onscene_time = row['On Scene DtTm']

            # search through file for date within date range & that have a non empty received and onscene time
            if date_start <= current_row_date <= date_end and received_time.strip() and onscene_time.strip():
                # calculate for Response Time
                # Received DtTm,Entry DtTm,Dispatch DtTm,Response DtTm,On Scene DtTm
                received_time = convertDateToHourMinuteSecond(received_time)
                onscene_time = convertDateToHourMinuteSecond(onscene_time)

                # if the received and oncscene time are exactly the same, report time of 0 seconds
                if onscene_time == received_time:
                    # print("times were the same: ", onscene_time, " -- ", received_time)
                    response_time_array.append(0)
                else:
                    # find difference between received and onscene time; convert to seconds
                    response_time_object = onscene_time - received_time
                    response_time = (response_time_object.days * 24 * 3600) + response_time_object.seconds

                    # only append response times that make sense (positive values only)
                    if response_time > 0:
                        # append the response time for the current row into an array
                        response_time_array.append(response_time)
                    else:
                        print("response time was not greater than zero: ", response_time, " received time: ", received_time, " onscene time: ", onscene_time, " unit id:", row['Unit ID'])
    return response_time_array


def calculatePercentileIndexValue(array):

    # sort in reverse order; smaller times = faster/better response
    array.sort(reverse = True)

    # store sorted array into new value
    sorted_array = array

    # find length of array
    array_length = len(array)

    # multiply 90 percent by the total number of values in array
    index_value = array_length * 0.9

    # round the index value to the nearest integer
    index_value = round(index_value)

    # find 90th percentile value from dataset
    ninety_percentile_value = sorted_array[index_value]

    return ninety_percentile_value


def mergedict(a,b):
    a.update(b)
    return a


def outputToCSV(Dict):

    print("Writing data to CSV...")

    csv_columns = ['EmergencyResponseDistrict', 'Month', '90th Percentile Response Time']


    with open('mysidewalk-output.csv', 'w', newline='') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter='\t')
        csvwriter.writerow(csv_columns)
        for session in Dict:
            for item in Dict[session]:
                csvwriter.writerow([session, item, Dict[session][item]])
    
    print("Finished creating CSV")


# create dictionary
Dict = {}

response_time = 0
total_responses = 0

# Create array with values of all calculated response times in given date range
response_time_array = createResponseTimeArray()

# Use response_time_array to determine the 90th percentile index value
# Every value equivalent or smaller will be considered in the '90th percentile'

# printed array here for *testing purposes*
# for x in range(len(response_time_array)):
#     print (response_time_array[x])

ninety_percentile_value = calculatePercentileIndexValue(response_time_array)

print("90th percentile value: ", ninety_percentile_value)

# print("response time array:")
# for x in range(len(response_time_array)):
#     print (response_time_array[x])

with open(filename) as csvfile:  
    data = csv.DictReader(csvfile)
    for row in data:
        # example date string: 07/25/2019 07:18:15 PM

        # convert date to year/month/day
        current_row_date = convertDateToYearMonthDay(row['Received DtTm'])

        # create start and end date for desired date range
        date_start = datetime(2019, 1, 1)
        date_end = datetime(2020, 1, 1)

        # example dictionary entry
        # Dict['B01'] = {'2019-01': 504, '2019-02': 580}

        received_time = row['Received DtTm']
        onscene_time = row['On Scene DtTm']

        # search through file for date within date range & that have a non empty received and onscene time
        if date_start <= current_row_date <= date_end and received_time.strip() and onscene_time.strip():
            

            # calculate for Response Time
            # Received DtTm,Entry DtTm,Dispatch DtTm,Response DtTm,On Scene DtTm
            received_time = convertDateToHourMinuteSecond(received_time)
            onscene_time = convertDateToHourMinuteSecond(onscene_time)

            response_time_object = onscene_time - received_time
            response_time = response_time_object.days * 24 * 3600 + response_time_object.seconds

            # only continue if the response time is equal or lower than the ninety percentile value
            if response_time <= ninety_percentile_value:
                unit_id = row['Unit ID']
                month = convertDateToYearMonth(row['Received DtTm'])

                # convert back to string so we can concatenate with unit id
                month = month.strftime('%Y/%m')

                key = unit_id 

                # Check if given key already exists in dictionary
                if checkKey(Dict, key):
                    if checkMonth(Dict, key, month):
                        # if true, add +1 to count of given unit/month key pair
                        temp_integer = Dict[key][month]
                        temp_integer += 1
                        Dict[key][month] = temp_integer
                        total_responses += 1
                    else:
                        Dict[key][month] = 1
                        total_responses += 1
                else:
                    # key doesn't not exist, create dictionary element for key, set count to 1
                    Dict[key] = {}
                    Dict[key][month] = 1
                    total_responses += 1




outputToCSV(Dict)


print("total responses: ", total_responses)



print("Program run time = {} seconds".format(time.time() - starttime))