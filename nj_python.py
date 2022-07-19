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
nj_df = old_nj_df[['date','time','location','subject_race', 'subject_sex','arrest_made','outcome','frisk_performed','search_conducted','vehicle_color','vehicle_make','violation']]

# Minimum and maximum date for NJ
nj_min_date=nj_df["date"].min() 
nj_max_date=nj_df["date"].max() 


# STOPS PER YEAR

num_of_stops_2009=nj_df.query('20090101 <= date <20100101' )
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
    per_capita.append((len(y_axis[i])/pop_by_year[i]))

num_stops_year=[]
for i in y_axis:
    num_stops_year=len(i)



'''f,ax=plt.subplots(1)
ax.plot(x_axis,per_capita)
plt.title("New Jersey Taffic Stop rate P2009-2016")
plt.xlabel("Year")
plt.ylabel("Traffic Rate")
ax.set_ylim(ymin=0)
plt.show()'''

#Number of stops by race
num_stops_race={}
for stop in nj_df['subject_race']:
    if stop in num_stops_race:
        num_stops_race[stop]+=1
    else:
        num_stops_race[stop]=1


num_stops_race={'black': 45119, 'unknown': 3697161, 'hispanic': 25955, 'white': 71929, 'asian/pacific islander': 5071, 'other': 99}

#Number of stops per year by race
num_stops_race_per_year=[]

rate_stops_race_per_year=[]
for year in y_axis:
    tmp={}
    for val in year['subject_race']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    num_stops_race_per_year.append(tmp) # adding the num of stop per race in year in array
    

for i in range(len(num_stops_race_per_year)):
    tmp={}
    for key in num_stops_race_per_year[i].keys():
        tmp[key]=(num_stops_race_per_year[i][key]/pop_by_year[i])
    rate_stops_race_per_year.append(tmp)

# RATE OF SEXES STOPPED PER YEAR + bar graph of number of stopped by sex 2009-2016
num_stops_sex_per_year=[]
for year in y_axis:
    tmp={}
    for val in year['subject_sex']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    num_stops_sex_per_year.append(tmp)
#print(num_stops_sex_per_year)

rate_stops_sex_per_year=[]
for i in range(len(num_stops_sex_per_year)):
    tmp={}
    for key in num_stops_sex_per_year[i].keys():
        tmp[key]=(num_stops_sex_per_year[i][key]/pop_by_year[i])
    rate_stops_sex_per_year.append(tmp)
#print(rate_stop_sex_per_year)

'''x_axis=["Male","Female","Unknown/Other"]
y_axis=list(sex_per_year.values())
plt.bar(x_axis,y_axis,color='brown')
plt.title('NUMBER OF STOPS PER SEX -NJ')
plt.xlabel('Genders')
plt.ylabel('Amount of Stops')
plt.show()

'''
# Veichicle color stopped
type_veh_colors_stopped={}
for color in nj_df['vehicle_color']:
    if color in type_veh_colors_stopped:
        type_veh_colors_stopped[color]+=1
    else:
        type_veh_colors_stopped[color]=1
#print(type_veh_colors_stopped)


# Number OF OUTCOMES 
num_outcomes={}
for oc in nj_df['outcome']:
    if oc in num_outcomes:
        num_outcomes[oc]+=1
    else:
        num_outcomes[oc]=1


num_outcomes_per_year=[]
for year in y_axis:
    tmp={}
    for val in year['outcome']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    num_outcomes_per_year.append(tmp)

#print(num_outcomes_per_year)
rate_outcomes_per_year=[]

for i in range(len(num_outcomes_per_year)):
    tmp={}
    for key in num_outcomes_per_year[i].keys():
        tmp[key]=(num_outcomes_per_year[i][key]/pop_by_year[i])
    rate_outcomes_per_year.append(tmp)



'''# Reasons for stops
violations=[]
for vio in nj_df['violation']:
    tmp={}
    if vio in violations:
        tmp[vio]+=1
    else:
        tmp[vio]=1
    violations.append(tmp)
with open("//Users/hudaali/Desktop/lonLat_nj.txt","w+") as tmp:
    tmp.write(str(violations))'''

# Writing results in notes file
with open("/Volumes/T7/Research/Research_programs/States/NEW JERSEY/nj_notes.txt","w+") as nj_notes:
    nj_notes.write("Minimum Sate:\n"+str(nj_min_date)+"\n")
    nj_notes.write("Maximum Date:\n"+str(nj_max_date)+"\n")
    nj_notes.write("Aproximation Population over 2009-2016:\n{}\n\n".format(pop_by_year))
    nj_notes.write("Number of Stops per Year:\n{}\n\n".format(num_stops_year))
    nj_notes.write("Rate of Stops per Year:\n{}\n\n".format(per_capita))
    nj_notes.write("Amount of stops by race\n2009-2016:{}\n\n".format(num_stops_race))
    nj_notes.write("Number of Stops by Race per Year:\n{}\n\n".format(num_stops_race_per_year))
    nj_notes.write("Rate of Stops by Race:\n{}\n\n".format(rate_stops_race_per_year))
    nj_notes.write("Number of Stops by Sex per Year:\n{}\n\n".format(num_stops_sex_per_year))
    nj_notes.write("Rate of Stops by Sex per Year:\n{}\n\n".format(rate_stops_sex_per_year))
    nj_notes.write("Number of outcomes per Year:\n{}\n\n".format(num_outcomes_per_year))
    nj_notes.write("Rate of outcomes per Year:\n{}\n\n".format(rate_outcomes_per_year))
    nj_notes.write("Types of cars Stopped:\n{}\n\n".format(type_veh_colors_stopped))

    
    

   
    
    



    
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



