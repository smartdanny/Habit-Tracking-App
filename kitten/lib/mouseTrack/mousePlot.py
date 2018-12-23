# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 11:31:10 2018
@author: Alexandra
"""
import matplotlib.pyplot as plt
import random
import pandas as pd
import seaborn as sns; sns.set(style="white", color_codes=True)
import mouseClickAndLocation #to get the csv path

df = pd.DataFrame()
df['x'] = pd.read_csv('../../data/mouseLoc.csv')['x']
df['y'] = pd.read_csv('../../data/mouseLoc.csv')['y']

g = sns.jointplot("x", "y", data=df[['x', 'y']], kind = "kde", space=0)
plt.show()
