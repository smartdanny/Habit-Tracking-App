"""
This script shows a simple example of a 3D plot of mouse location using matplotlib

This script relies on the datapath outlined in mouseClickAndLocation for .csv files
as well as csvToDataFrame in order to create a df.
@author: James
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csvToDataFrameExample

# EXAMPLE
#Getting dataframe
df = csvToDataFrameExample.read_from_CSV('mouseLoc.csv') #get the dataframe
csvToDataFrameExample.pd.set_option('display.float_format', lambda x: '%.7f' % x) #make sure scientific notation is off

#Plotting 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.plot(df['X'], df['Y'], zs=df['Time'])
plt.show()
