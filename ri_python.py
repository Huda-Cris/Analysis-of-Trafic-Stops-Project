import csv
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


with open ("/Volumes/T7/Research/Research_programs/States/RHODE ISLAND/ri_statewide_2020_04_01.csv", "r+") as ri_csv:
    ri=pd.read_csv(ri_csv)
    old_ri_df=pd.DataFrame(ri)

old_ri_df['date'] = pd.to_datetime(old_ri_df['date'], format='%Y-%m-%d')


ri_df = old_ri_df[['date','time','subject_race', 'subject_sex','arrest_made','outcome','contraband_found','search_conducted','frisk_performed','search_conducted','reason_for_search','reason_for_stop']]
ri_max_date=ri_df['date'].max()
ri_min_date=ri_df['date'].min()
print(old_ri_df.columns)