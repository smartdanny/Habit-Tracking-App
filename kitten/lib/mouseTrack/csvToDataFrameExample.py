'''
This script shows an example of how to read the data from a .csv file into a DataFrame
as well as adjust the times from relative difference to timestamps.
'''

import pandas as pd
import datetime
import csv
import lib.mouseTrack.mouseClickAndLocation as clickAndLoc #to get the csv path

def read_from_CSV(csvFileName):
    '''
    This function takes the name of a csv file with a path and returns
    a dataframe loaded with the information from that file
    '''
    values = []
    date = []
    #Open the .csv file
    with open(clickAndLoc.csvPath + csvFileName) as f:
        reader = csv.reader(f)
        columnNames = next(reader) # get the column names
        values = [list(map(float, row)) for row in csv.reader(f)] # read in floats to array
        
    # Recalculate the time since epoch into timestamps
    date.append(datetime.datetime.fromtimestamp(values[0][0]))
    for i in range(1, len(values)):
        values[i][0] = values[i-1][0] + values[i][0]
        date.append(datetime.datetime.fromtimestamp(values[i][0])) # create an array of timestamps too
    df = pd.DataFrame(values, columns = columnNames) # create dataframe with values and columns
    df['Time'] = date # assign time stamps
    return df

# EXAMPLE
# df = read_from_CSV('mouseLoc.csv') #get the dataframe
# pd.set_option('display.float_format', lambda x: '%.7f' % x) #make sure scientific notation is off
# print(df) #print the data frame
