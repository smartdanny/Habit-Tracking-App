"""
This script shows a simple example of a 3D plot of mouse location using matplotlib

This script relies on the datapath outlined in mouseClickAndLocation for .csv files
as well as csvToDataFrame in order to create a df.
@author: James
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import lib.mouseTrack.csvToDataFrameExample as csv

# EXAMPLE
#Getting dataframe
df = csv.read_from_CSV('mouseLoc.csv') #get the dataframe
csv.pd.set_option('display.float_format', lambda x: '%.7f' % x) #make sure scientific notation is off

print(df)

#Plotting 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.plot(df['x'], df['y'], zs=df['Time'])
plt.show()
