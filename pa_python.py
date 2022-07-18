import csv
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


with open ("/Volumes/T7/Research/Research_programs/States/PENNSYLVANIA/pa_philadelphia_2020_04_01.csv", "r+") as pa_csv:
    pa=pd.read_csv(pa_csv)
    old_pa_df=pd.DataFrame(pa)

old_pa_df['date'] = pd.to_datetime(old_pa_df['date'], format='%Y-%m-%d')


pa_df = old_pa_df[['date','time','location','subject_age','subject_race', 'subject_sex','arrest_made','outcome','contraband_found','search_conducted','search_person','search_vehicle']]
pa_max_date=pa_df['date'].max()
pa_min_date=pa_df['date'].min()



# getting stops per location
def pa_stopsPerLoc():
    locations={}
    for twp in pa_df['location']:
        # place=convert(twp)
        if twp in locations:
            locations[twp]+=1
        else:
            locations[twp]=1

    with open("/Users/hudaali/Desktop/Dict.txt",'w+') as dict:
        for key in locations.items():
            dict.write(str(key))

pa_stopsPerLoc()