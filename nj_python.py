from scipy.optimize import curve_fit
import pandas as pd
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="MyApp")


with open ("/Volumes/T7/Research/Research_programs/States/NEW JERSEY/nj_statewide_2020_04_01.csv", "r") as nj_csv:
    nj=pd.read_csv(nj_csv)

old_nj_df=pd.DataFrame(nj)
old_nj_df['date'] = pd.to_datetime(old_nj_df['date'], format='%Y-%m-%d') # convert dates into a DATETIME

# Columns needed for NJ
nj_df = old_nj_df[['date','time','location','subject_race', 'subject_sex','arrest_made','outcome','frisk_performed','search_conducted','vehicle_color','vehicle_make']]

# Minimum and maximum date for NJ
nj_min_date=nj_df["date"].min() 
nj_max_date=nj_df["date"].max() 


# STOPS PER YEAR

num_of_stops_2009=nj_df.query('20090101 <= date <20100101')
num_of_stops_2010=nj_df.query('20100101 <= date <20110101')
num_of_stops_2011=nj_df.query('20110101 <= date <20120101')
num_of_stops_2012=nj_df.query('20120101 <= date <20130101')
num_of_stops_2013=nj_df.query('20130101 <= date <20140101')
num_of_stops_2014=nj_df.query('20140101 <= date <20150101')
num_of_stops_2015=nj_df.query('20150101 <= date <20160101')
num_of_stops_2016=nj_df.query('20160101 <= date <20170101')
x_axis=[2009,2010,2011,2012,2013,2014,2015,2016] # number of years
y_axis=[num_of_stops_2009,num_of_stops_2010,num_of_stops_2011,num_of_stops_2012,num_of_stops_2013,num_of_stops_2014,num_of_stops_2015,num_of_stops_2016]
# bar Graph of number of stopr per year
'''
plt.bar(x_axis,y_axis,color='brown')
plt.title('Number of Traffic Stops per Year -NJ')
plt.xlabel('Years')
plt.ylabel('Amount of Stops')
plt.show()'''



# STOPS PER CAPITA
per_capita=[]
pop_by_year=[8750000,8791000,8753000,8794000,8832000,8874000,8904000,8915000]
for i in range(len(pop_by_year)):
    per_capita.append((len(y_axis[i])/pop_by_year[i])*100000)

dates=nj_df['date']



f,ax=plt.subplots(1)
ax.plot(x_axis,per_capita)
plt.title("New Jersey Taffic Stop rate P2009-2016")
plt.xlabel("Year")
plt.ylabel("Traffic Rate")
ax.set_ylim(ymin=0)
plt.show()

#Number of stops by race
'''num_stops_race={}
for stop in nj_df['subject_race']:
    if stop in num_stops_race:
        num_stops_race[stop]+=1
    else:
        num_stops_race[stop]=1'''

num_stops_race={'black': 45119, 'unknown': 3697161, 'hispanic': 25955, 'white': 71929, 'asian/pacific islander': 5071, 'other': 99}

#Number of stops per year by race
'''rate_stops_race_per_year=[]
for year in y_axis:
    tmp={}
    for val in year['subject_race']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    rate_stops_race_per_year.append(tmp)'''

# RATE OF SEXES STOPPED PER YEAR + bar graph of number of stopped by sex 2009-2016
'''rate_stops_sex_per_year=[]
for year in y_axis:
    tmp={}
    for val in year['subject_sex']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    rate_stops_sex_per_year.append(tmp)

sex_per_year={}
for sex in nj_df['subject_sex']:
    if sex in sex_per_year:
        sex_per_year[sex]+=1
    else:
        sex_per_year[sex]=1
print(sex_per_year)
x_axis=["Male","Female","Unknown/Other"]
y_axis=list(sex_per_year.values())
plt.bar(x_axis,y_axis,color='brown')
plt.title('NUMBER OF STOPS PER SEX -NJ')
plt.xlabel('Genders')
plt.ylabel('Amount of Stops')
plt.show()'''


# Veichicle color stopped
'''veh_colors_stopped={}
for color in nj_df['vehicle_color']:
    if color in veh_colors_stopped:
        veh_colors_stopped[color]+=1
    else:
        veh_colors_stopped[color]=1
print(veh_colors_stopped)'''


# RATE OF OUTCOMES 
'''outcomes={}
for oc in nj_df['outcome']:
    if oc in outcomes:
        outcomes[oc]+=1
    else:
        outcomes[oc]=1

rate_outcomes_per_year=[]
for year in y_axis:
    tmp={}
    for val in year['outcome']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    rate_outcomes_per_year.append(tmp)

print(rate_outcomes_per_year)'''

# Writing results in notes file
'''with open("/Volumes/T7/Research/Research_programs/States/NEW JERSEY/nj_notes.txt","a+") as nj_notes:
    #nj_notes.write("NUMBER OF STOPS PER RACE 2009-2016:\t" + str(num_stops_race)+"\n\n")
    #nj_notes.write("RATE OF STOPS PER YEAR:\t"+ str(per_capita)+"\n\n")
    #nj_notes.write("NUMBER OF STOPS PER YEAR: "+str(y_axis)+"\n\n")
    #nj_notes.write("RATE STOPS PER RACE PER YEAR: "+ str(rate_stops_race_per_year)+"\n\n")
    #nj_notes.write("RATE OF STOPS BY SEX PER YEAR: " +str(rate_stops_sex_per_year)+"\n\n")
    #nj_notes.write("TYPES OF VEHCLIE COLORS STOPPED: " +str(veh_colors_stopped)+"\n\n")
    #nj_notes.write("TYPES OF OUTCOMES: " +str(outcomes)+"\n\n")
    # nj_notes.write("RATE OF OUTCOMES PER YEAR: "+str(rate_outcomes_per_year)+"\n\n")'''
#STOPS PER LOCATION
"""def convert(lst):
    tmp=lst.rfind(',')
    return lst[tmp+1:]
locations={}
def nj_stopsPerLoc():
    for twp in nj_df['location']:
        place=convert(twp).strip()
        if place in locations:
            locations[place]+=1
        else:
            locations[place]=1"""




# latitude/longitude for map plot  ---Come back when developing website
# use google maps api for this

'''keys=list(locations.keys())
key=geolocator.geocode(keys[0]+" NJ")
print(key.latitude)
long=[]
lat=[]
no=[]
with open("/Users/hudaali/Desktop/lonLat_nj.txt","w+") as locoNJ:
    locoNJ.write("hi")
def get_LongLat():
   for i in range(len(keys)):
    addr=geolocator.geocode(str(keys[i])+" NJ")
    if addr is None:
        no.append(addr)
        print(i)
        break  
get_LongLat()
print(no)'''


# Reasons for stops
'''vilation=[]
for i in range(1000):
    if((str(old_nj_df['violation'][i])).lower() =='nan'):
        continue
    else:
        vilation.append(old_nj_df['violation'][i])
'''
