import pandas as pd
from mouseTrack import mouseClickAndLocation #to get the csv path

def read_from_CSV(csvFileName):
    df = pd.read_csv(mouseClickAndLocation.csvPath + csvFileName);
    return df

# EXAMPLE
# df = read_from_CSV('mouseLoc.csv') #get the dataframe
# pd.set_option('display.float_format', lambda x: '%.7f' % x) #make sure scientific notation is off
# print(df) #print the data frame
