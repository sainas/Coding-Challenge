# Introduction
# First, open actual.txt and predicted.txt.
# Then, for datas of each hour, we do the following things:
# Start from the actual price.
# Read all the data in one hour and store the stock ids and prices in 'input_dict'
# Then check if the predicted stock ids are in the dictionary.
# If so we calculate the error and update the 'timewindow' array
# Calculate a window_average error and store in 'output_list'
# Go to the data of next hour.

# After reading all the lines in both files, write 'output_list' into 'comparison.txt'

# Structure of timewindow
# The number of rows is decided by given window size
# timewindow[:,0] is current time
# timewindow[:,1] is the sum of error per hour
# timewindow[:,2] is the number of error added



# Created by Saina

import numpy as np
import sys
import time

def Is_str_digit(A):
    """
    function that checks if the string is a digit or not
    """
    if A is "":
        return False
    else:
        B = A.replace('.', '', 1)
        if B[0] == "-":                # in case the string is a minus digit
            B = B.replace('-', '', 1)
        return B.isdigit()

def splitData(line):
    """
    function that splits a long string by "|", and then changes the data type.
    """
    line = line.strip('\n')
    time, name, value = line.split("|")
    time = int(time)
    if Is_str_digit(value) is True:       # skip bad data
        value = float(value)
    else:
        value = None
        print(line, 'value is not digit')

    return time, name, value

def output_per_window(current_time, timewindow):
    """
    function that calculates the average error and return one line output string
    """
    if np.sum(timewindow[:, 2]) == 0:
        ave_error = 'na'
    else:
        ave_error = str(format((np.sum(timewindow[:, 1]) / np.sum(timewindow[:, 2])), '.2f'))

    output_seq = str(current_time - timewindow.shape[0]), str(current_time - 1),ave_error
    return "|".join(output_seq)


def main():
    start = time.clock()

    WINDOW_PATH = sys.argv[1]
    INPUT_PATH = sys.argv[2]
    PRE_PATH = sys.argv[3]
    OUTPUT_PATH = sys.argv[4]

    # get the size of window
    filewindow = open(WINDOW_PATH)
    windowSize = int(filewindow.read())
    filewindow.close()

    # initialization
    start_time = None
    current_time = None
    input_dict = {}
    timewindow = np.zeros((windowSize, 3))
    output_list = []

    with open(PRE_PATH,"r") as fileprd:
        with open(INPUT_PATH,"r") as filein:
            line_prd = fileprd.readline()
            prd_time, prd_name, prd_value = splitData(line_prd)
            for line_in in filein:
                input_time, input_name, input_value = splitData(line_in)

                if start_time is None:            # in case the time isn't start from 1
                    start_time = input_time
                    current_time = start_time

                if input_time == current_time:
                    input_dict[input_name] = input_value

                else:
                    sum_error = 0
                    num_of_prd = 0
                    while(prd_time == current_time):
                        if (input_dict.get(prd_name, None) is not None and prd_value is not None):
                            sum_error = sum_error + abs(input_dict.get(prd_name) - prd_value)
                            num_of_prd += 1
                        line_prd = fileprd.readline()
                        if not line_prd:              # in case the 'predicted.txt' ends
                            break
                        prd_time, prd_name, prd_value = splitData(line_prd)
                    timewindow[current_time % windowSize] = current_time, sum_error, num_of_prd
                    current_time += 1
                    input_dict = {}
                    input_dict[input_name] = input_value

                    if current_time >= start_time + windowSize:
                        output_list.append(output_per_window(current_time, timewindow))

        if filein.closed:    # After the final hour the 'actual.txt' will close. But
            sum_error = 0    # the predicted data of final hour hasn't be processed
            num_of_prd = 0
            while (prd_time == current_time):
                if (input_dict.get(prd_name, None) is not None and prd_value is not None):
                    sum_error = sum_error + abs(input_dict.get(prd_name) - prd_value)
                    num_of_prd += 1
                line_prd = fileprd.readline()
                if not line_prd:         # in case the 'predicted.txt' ends
                    break
                prd_time, prd_name, prd_value = splitData(line_prd)
                
            timewindow[current_time % windowSize] = current_time, sum_error, num_of_prd
            current_time += 1

            if current_time >= start_time + windowSize:
                output_list.append(output_per_window(current_time, timewindow))


    fileout = open(OUTPUT_PATH, "w")
    fileout.write("\n".join(output_list))
    fileout.close()

    elapsed = (time.clock() - start)
    print("Time used:",elapsed)

if __name__ == '__main__':
    main()