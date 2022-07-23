import csv
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

path = "/Users/hudaali/Downloads/ny_statewide_2020_04_01.csv"

#generates connectticut csv files
with open (path, "r") as ny_df:
    df=pd.read_csv(ny_df)

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')   
print(df['date'])