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


    df = pd.read_csv(csvFileName, error_bad_lines=False, delimiter=',')

    # Recalculate the time since epoch into timestamps
    [rows, columns] = df.shape
    print(rows)
    timeStamp = [0] * rows
    timesFloat = [0] * rows

    timesFloat[0] = df.iloc[0]['Time']
    timeStamp[0] = datetime.datetime.fromtimestamp(df.iloc[0]['Time'])
    for i in range(1, rows):
        # print(i)
        timesFloat[i] = timesFloat[0] + df.iloc[i]['Time']
        timeStamp[i] = datetime.datetime.fromtimestamp(timesFloat[i]) # create an array of timestamps too

    lastTime = timesFloat[len(timesFloat)-1]
    firstTime = timesFloat[0]

    df['Time'] = timeStamp
    print(df)
    return df, lastTime, firstTime

# EXAMPLE
# df = read_from_CSV('mouseLoc.csv') #get the dataframe
# pd.set_option('display.float_format', lambda x: '%.7f' % x) #make sure scientific notation is off
# print(df) #print the data frame
