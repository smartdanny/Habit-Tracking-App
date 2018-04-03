import pandas as pd
import lib.mouseTrack.mouseClickAndLocation as clickAndLoc #to get the csv path

def read_from_CSV(csvFileName):
    df = pd.read_csv(clickAndLoc.csvPath + csvFileName);
    df['Time'] = pd.to_datetime(df['Time'])
    return df

# EXAMPLE
# df = read_from_CSV('mouseLoc.csv') #get the dataframe
# pd.set_option('display.float_format', lambda x: '%.7f' % x) #make sure scientific notation is off
# print(df) #print the data frame
