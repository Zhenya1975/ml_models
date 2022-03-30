import pandas as pd
from scipy import *
import numpy as np


data_df = pd.read_csv("data/motohours_data_eo.csv")
# print(data_df.info())
# print(len(data_df))
# на графике получившихся точек видны выбросы. убираем их
data_df = data_df.loc[data_df['motohours_measure_ts'] > 50000000]
# print(len(data_df))
data_df = data_df.loc[:, ['motohours_measure_ts', 'motohours']]
data_df.sort_values(['motohours_measure_ts'], inplace = True)

x = data_df['motohours_measure_ts'].values
y = data_df.motohours

p1 = np.polyfit(x,y,1)
# print(p1)

p2 = np.polyfit(x,y,2)
# np.set_printoptions(precision = 15, suppress= True)


p3 = np.polyfit(x,y,3)
# print(p3)
