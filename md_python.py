import csv
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


with open ("/Volumes/T7/Research/Research_programs/States/MARYLAND/md_statewide_2020_04_01.csv", "r+") as md_csv:
    md=pd.read_csv(md_csv)
    old_md_df=pd.DataFrame(md)

old_md_df['date'] = pd.to_datetime(old_md_df['date'], format='%Y-%m-%d')

md_df = old_md_df[['date','time','department_name','subject_age','subject_race', 'subject_sex','violation','arrest_made','outcome','contraband_found','search_conducted','search_person','search_vehicle','reason_for_stop','reason_for_search','reason_for_arrest']]
md_max_date=md_df['date'].max()
md_min_date=md_df['date'].min()

'''
print(md_df['department_name'].iloc[10000:10090])'''


def convert(lst):
    tmp=lst.rfind(' ')
    return lst[:tmp+1]

def md_stopsPerLoc():
    locations={}
    for twp in md_df['department_name']:
        place=convert(twp)
        if place in locations:
            locations[place]+=1
        else:
            locations[place]=1

    with open("/Users/hudaali/Desktop/Dict.txt",'w+') as dict:
        for key in locations.items():
            dict.write(str(key))

md_stopsPerLoc()