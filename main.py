import csv  
import os
import time
from datetime import datetime, timedelta
import itertools
import sys


# Copy input data file into the same directory as this python program.
# Replace 'Fire_Department_Calls_for_Service.csv' (line 14) with the name for your input file.
# Run program by calling the path to your python3 followed by the name of this program.
# i.e. 'C:/Users/Andrew/AppData/Local/Programs/Python/Python38-32/python.exe c:/Users/Andrew/OneDrive/Desktop/mysidewalk/main.py'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'Fire_Department_Calls_for_Service.csv')
# my_file = os.path.join(THIS_FOLDER, 'small_example_input.csv')
# define the name of the file to read from
filename = my_file


# use datetime module to convert string to desired datetime object
def convertDateToYearMonthDay(date_string):
    # save date string into date object: current_row_date
    current_row_date = datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
    # convert date to string, only save year/month/day
    current_row_date = current_row_date.strftime('%Y/%m/%d')
    # convert from string back to datetime object
    current_row_date = datetime.strptime(current_row_date, '%Y/%m/%d')
    return current_row_date


# use datetime module to convert string to desired datetime object
def convertDateToYearMonth(date_string):
    # save date string into date object: current_row_date
    current_row_date = datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
    # convert date to string, only save year/month/day
    current_row_date = current_row_date.strftime('%Y/%m')
    # convert from string back to datetime object
    current_row_date = datetime.strptime(current_row_date, '%Y/%m')
    return current_row_date


# use datetime module to convert string to desired datetime object
def convertDateToHourMinuteSecond(date_string):
    # save date string into date object: current_row_date
    current_row_date = datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
    return current_row_date


# check if key (unit id) is in dictionary
def checkKey(dict, key):
    if key in dict:
        return True
    else:
        return False


# check if month is in dictionary given the key and month
def checkMonth(dict, key, month):
    if month in dict[key]:
        return True
    else:
        return False

# create and return an array of all valid response times (onscene_time - received_time)
# response times that were non-positive were considered invalid and saved to error dictionary
def createResponseTimeArray():
    response_time_array = []
    reading_data_logging_count = 0
    print("Populating array with valid response times...")

    with open(filename) as csvfile:  
        data = csv.DictReader(csvfile)
        for row in data:
            # create logging for during CSV input
            reading_data_logging_count += 1
            if(reading_data_logging_count % 1000000 == 0):
                print(reading_data_logging_count, " rows of data read from input CSV file")

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
                received_time = convertDateToHourMinuteSecond(received_time)
                onscene_time = convertDateToHourMinuteSecond(onscene_time)

                # if the received and oncscene time are exactly the same, zero second response, save to error dictionary
                if onscene_time == received_time:
                    savingToDictionary(row, response_time_error_dict)
                else:
                    # find difference between received and onscene time; convert to seconds
                    response_time_object = onscene_time - received_time
                    response_time = (response_time_object.days * 24 * 3600) + response_time_object.seconds

                    # only append response times that make sense (positive values only)
                    if response_time > 0:
                        # append the response time for the current row into an array
                        response_time_array.append(response_time)
                    else:
                        savingToDictionary(row, response_time_error_dict)
    print("Finished creating array of valid response times")
    return response_time_array


# sort response time array, find and return the 90th percentile value
def calculatePercentileIndexValue(array):

    print("Sorting array of valid response times...")
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

    print("90th percentile value has been found")
    return ninety_percentile_value

# write data from dictionary to CSV, using appropriate sorted keys
def outputToCSV(Dict, dict_keys, outputFileName, thirdColumnName):

    print("Writing data to CSV...")

    csv_columns = ['EmergencyResponseDistrict', 'Month', thirdColumnName]

    with open(outputFileName, 'w', newline='') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter='\t')
        csvwriter.writerow(csv_columns)
        for session in dict_keys:
            for item in Dict[session]:
                csvwriter.writerow([session, item, Dict[session][item]])
    
    print("Finished creating CSV")


# Saving count of 90th percentile response times in dictionary
def savingToDictionary(row, dictionary):
    unit_id = row['Unit ID']
    month = convertDateToYearMonth(row['Received DtTm'])

    # convert back to string so we can concatenate with unit id
    month = month.strftime('%Y/%m')
    key = unit_id 

    # Check if given key already exists in dictionary
    if checkKey(dictionary, key):
        if checkMonth(dictionary, key, month):
            # if true, add +1 to count of given unit/month key pair
            temp_integer = dictionary[key][month]
            temp_integer += 1
            dictionary[key][month] = temp_integer
        else:
            dictionary[key][month] = 1
    else:
        # key doesn't not exist, create dictionary element for key, set count to 1
        dictionary[key] = {}
        dictionary[key][month] = 1


# main function
def main():

    # start time is created so that we can track the runtime of our program
    starttime = time.time()

    # create dictionary
    Dict = {}

    # global variable is created so that it can be used in other functions
    global response_time_error_dict
    response_time_error_dict = {}
    response_time = 0

    # Create array with values of all calculated response times in given date range
    response_time_array = createResponseTimeArray()

    # Use response_time_array to determine the 90th percentile index value
    # Every value equivalent or smaller will be considered in the '90th percentile'
    ninety_percentile_value = calculatePercentileIndexValue(response_time_array)

    print("The 90th percentile value is: ", ninety_percentile_value)

    with open(filename) as csvfile:  
        reading_data_logging_count = 0
        data = csv.DictReader(csvfile)
        print("Reading data from input CSV file...")
        for row in data:
            # create logging for during CSV input
            reading_data_logging_count += 1
            if(reading_data_logging_count % 1000000 == 0):
                print(reading_data_logging_count, " rows of data read from input CSV file")

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
                    savingToDictionary(row, Dict)
        print("Finished reading data from input file")

    # save the sorted keys (unit ids) of each dictionary
    # use these keys later to output to CSV in sorted order by Unit ID
    dict_keys = sorted(Dict.keys())
    error_keys = sorted(response_time_error_dict.keys())

    # output each dictionary to CSV file
    outputToCSV(Dict, dict_keys, 'main_output.csv', '90th Percentile Response Time')
    outputToCSV(response_time_error_dict, error_keys, 'errors_output.csv', 'Error: Negative or Zero Response Time')

    print("Program run time = {} seconds".format(time.time() - starttime))


# call the main function
main()