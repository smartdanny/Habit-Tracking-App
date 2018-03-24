# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 11:31:10 2018

@author: Alexandra
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set(style="white", color_codes=True)
import mouseClickAndLocation #to get the csv path

def read_from_CSV(csvFileName):
    df = pd.read_csv(mouseClickAndLocation.csvPath + csvFileName);
    return df

# EXAMPLE
df = read_from_CSV('mouseLoc.csv') #get the dataframe
pd.set_option('display.float_format', lambda x: '%.7f' % x) #make sure scientific notation is off
print(df) #print the data frame

df.head()
sns.jointplot(x="x", y="y", data=df)