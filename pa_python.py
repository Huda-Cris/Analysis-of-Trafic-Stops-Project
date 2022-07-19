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


pa_df = old_pa_df[['date','time','location','subject_age','subject_race', 'subject_sex','arrest_made','outcome','contraband_found','search_conducted','search_person','search_vehicle','type']]

pa_df=pa_df.loc[(pa_df['date'] >= '2014-01-01') & (pa_df['date'] <= '2017-12-31') & (pa_df['type']=='vehicular')] #filtered data file
pa_max_date=pa_df['date'].max()#2018-04-14 00:00:00
pa_min_date=pa_df['date'].min()#2014-01-01 00:00:00

#Aprox population 
aprox_pa_pop_year=[1547000,1555000,1556000,1570000]
years=[2014,2015,2016,2017]

# NUMBER OF STOPS PER YEAR
num_of_stops_2014=pa_df.query('20140101 <= date <20150101')
num_of_stops_2015=pa_df.query('20150101 <= date <20160101')
num_of_stops_2016=pa_df.query('20160101 <= date <20170101')
num_of_stops_2017=pa_df.query('20170101 <= date <20180101')
num_stops_year=[num_of_stops_2014,num_of_stops_2015,num_of_stops_2016,num_of_stops_2017]

#  RATE OF STOPS  PER YEAR
rate_stops_per_year=[]

for i in range (len(aprox_pa_pop_year)):
    rate_stops_per_year.append(len(num_stops_year[i])/aprox_pa_pop_year[i])

# NUMBER OF STOPS PER RACE
num_stops_race_per_year=[]
for year in num_stops_year:
    tmp={}
    for val in year['subject_race']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    num_stops_race_per_year.append(tmp)

# RATE OF STOPS PER RACE PER YEAR
rate_stops_race_per_year=[]
for i in range(len(num_stops_race_per_year)):
    tmp={}
    for key in num_stops_race_per_year[i].keys():
        tmp[key]=(num_stops_race_per_year[i][key]/aprox_pa_pop_year[i])
    rate_stops_race_per_year.append(tmp)

# NUMBER OF STOPS BY SEX PER YEAR
num_stops_sex_per_year=[]
for year in num_stops_year:
    tmp={}
    for val in year['subject_sex']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    num_stops_sex_per_year.append(tmp)

# RATE OF STOPS PER RACE PER YEAR
rate_stops_sex_per_year=[]
for i in range(len(num_stops_sex_per_year)):
    tmp={}
    for key in num_stops_sex_per_year[i].keys():
        tmp[key]=(num_stops_sex_per_year[i][key]/aprox_pa_pop_year[i])
    rate_stops_sex_per_year.append(tmp)



#NUMBER OF TIMES VEICLES WERE SEARCHED
veh_search={}
for search in pa_df['search_vehicle']:
    if search in veh_search:
        veh_search[search]+=1
    else:
        veh_search[search]=1
print(veh_search)

#NUMBER OF TIMES VEICLES WERE SEARCHED Per YEAR
num_veh_search_year=[]
for year in num_stops_year:
    tmp={}
    for val in year['search_vehicle']:
        if val in tmp:
            tmp[val]+=1
        else:
            tmp[val]=1
    num_veh_search_year.append(tmp)


with open("/Volumes/T7/Research/Research_programs/States/PENNSYLVANIA/pa_notes.txt",'w+') as pa_notes:
    pa_notes.write("MINIMUM DATE:\n{}\n\n".format(pa_min_date))
    pa_notes.write("MAXIMUM DATE:\n{}\n\n".format(pa_max_date))
    pa_notes.write("APROXIMATION POPLUATION PER YEAR:\n{}\n\n".format(aprox_pa_pop_year))
    pa_notes.write("NUMBER OF STOPS PER RACE PER YEAR:\n{}\n\n".format(num_stops_race_per_year))
    pa_notes.write("RATE OF STOPS PER RACE PER YEAR:\n{}\n\n".format(rate_stops_race_per_year))
    pa_notes.write("NUMBER OF STOPS PER SEX PER YEAR:\n{}\n\n".format(num_stops_sex_per_year))
    pa_notes.write("RATE OF STOPS PER SEX PER YEAR:\n{}\n\n".format(rate_stops_sex_per_year))
    pa_notes.write("NUMBER OF VEHICLES SEARCHED PER YEAR:\n{}\n\n".format(num_veh_search_year))
    
'''# getting stops per location
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
            dict.write(str(key))'''
