from scipy.optimize import curve_fit
import pandas as pd
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="MyApp")


with open ("/Users/hudaali/Downloads/nj_statewide_2020_04_01.csv", "r") as nj_csv:
    nj=pd.read_csv(nj_csv)

old_nj_df=pd.DataFrame(nj)
old_nj_df['date'] = pd.to_datetime(old_nj_df['date'], format='%Y-%m-%d') # convert dates into a DATETIME
print(old_nj_df.columns)
# Columns needed for NJ
nj_df = old_nj_df[['date','time','location','subject_race', 'subject_sex','arrest_made','outcome','frisk_performed','search_conducted','vehicle_color','vehicle_make','violation','contraband_found']]

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
years=[2009,2010,2011,2012,2013,2014,2015,2016] # number of years
num_stops_year=[num_of_stops_2009,num_of_stops_2010,num_of_stops_2011,num_of_stops_2012,num_of_stops_2013,num_of_stops_2014,num_of_stops_2015,num_of_stops_2016]
# bar Graph of number of stop per year
'''
plt.bar(x_axis,y_axis,color='brown')
plt.title('Number of Traffic Stops per Year -NJ')
plt.xlabel('Years')
plt.ylabel('Amount of Stops')
plt.show()'''




rate_stops_per_year=[]
aprox_nj_pop_year=[8750000,8791000,8753000,8794000,8832000,8874000,8904000,8915000]
aprox_pop_by_race={
    'black':[],
    'white':[],
    'hispanic':[],
    'asian/pacific Islander':[],
    'other':[]
    }
for pop in aprox_nj_pop_year:
    for key in aprox_pop_by_race:
        if key=='black':
            aprox_pop_by_race[key].append(0.129*pop)
        elif key=='white':
            aprox_pop_by_race[key].append(pop*0.5815)
        elif key=='hispanic':
            aprox_pop_by_race[key].append(0.185*pop)
        elif key=='asian/pacific Islander':
            aprox_pop_by_race[key].append(pop*0.0885)
        elif key=='other':
            aprox_pop_by_race[key].append(pop*0.026)



# NUMBER OF STOPS PER YEAR
for i in range(len(aprox_nj_pop_year)):
    rate_stops_per_year.append((len(num_stops_year[i])/aprox_nj_pop_year[i]))





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


num_stops_race={'black': 45119, 'unknown': 3697161, 'hispanic': 25955, 'white': 71929, 'asian/pacific Islander': 5071, 'other': 99}

#NUMBER OF STOPS PER YEAR PER RACE
num_stops_race_per_year=[]

rate_stops_race_per_year=[]
for year in num_stops_year:
    tmp={}
    for val in year['subject_race']:
        if val not in tmp:
            tmp[val]=1
        else:
            tmp[val]+=1
    num_stops_race_per_year.append(tmp) # adding the num of stop per race in year in array
    
# RATE OF STOPS PER YEAR PER RACE
for i in range(len(num_stops_race_per_year)):
    tmp={}
    for key in num_stops_race_per_year[i].keys():
        tmp[key]=(num_stops_race_per_year[i][key]/len(nj_df))
    rate_stops_race_per_year.append(tmp)


#STOP RATE IN PORTPORTION TO POP RACE 
num_bk_stopped=len(nj_df.loc[nj_df['subject_race']=='black'])
num_yt_stopped=len(nj_df.loc[nj_df['subject_race']=='white'])
num_hp_stopped=len(nj_df.loc[nj_df['subject_race']=='hispanic'])
num_ap_stopped=len(nj_df.loc[nj_df['subject_race']=='asian/pacific Islander'])
num_ot_stopped=len(nj_df.loc[nj_df['subject_race']=='other'])
tmp_above=[num_bk_stopped,num_yt_stopped,num_hp_stopped,num_ap_stopped,num_ot_stopped]

race_names=["black","white","hispanic","asian/pacific Islander","other"]
stop_rate_race_porp_pop={
    'black':[],
    'white':[],
    'hispanic':[],
    'asian/pacific Islander':[],
    'other':[]
    }


for i in aprox_pop_by_race['black']:
    stop_rate_race_porp_pop['black'].append(num_bk_stopped/i)
for i in aprox_pop_by_race['white']:
    stop_rate_race_porp_pop['white'].append(num_yt_stopped/i)
for i in aprox_pop_by_race['hispanic']:
    stop_rate_race_porp_pop['hispanic'].append(num_hp_stopped/i)
for i in aprox_pop_by_race['asian/pacific Islander']:
    stop_rate_race_porp_pop['asian/pacific Islander'].append(num_ap_stopped/i)
for i in aprox_pop_by_race['other']:
    stop_rate_race_porp_pop['other'].append(num_ot_stopped/i)


# RATE OF SEXES STOPPED PER YEAR + bar graph of number of stopped by sex 2009-2016
num_stops_sex_per_year=[]
for year in num_stops_year:
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
        tmp[key]=(num_stops_sex_per_year[i][key]/(len(nj_df)))
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
#SEARCH  RATE
search_conducted=len(nj_df.loc[(nj_df['search_conducted']==True)])
search_conducted_bk=len(nj_df.loc[(nj_df['search_conducted']==True) & (nj_df['subject_race']=='black')])
search_conducted_yt=len(nj_df.loc[(nj_df['search_conducted']==True) & (nj_df['subject_race']=='white')])
search_conducted_hp=len(nj_df.loc[(nj_df['search_conducted']==True) & (nj_df['subject_race']=='hispanic')])
search_conducted_ap=len(nj_df.loc[(nj_df['search_conducted']==True) & (nj_df['subject_race']=='asian/pacific Islander')])
search_conducted_ot=len(nj_df.loc[(nj_df['search_conducted']==True) & (nj_df['subject_race']=='other') | (nj_df['subject_race']=='unknown')])

search_rates=[]
search_rates.append(search_conducted_bk/search_conducted)
search_rates.append(search_conducted_yt/search_conducted)
search_rates.append(search_conducted_hp/search_conducted)
search_rates.append(search_conducted_ap/search_conducted)
search_rates.append(search_conducted_ot/search_conducted)


#Frisk Rate

frisk_performed=len(nj_df.loc[(nj_df['frisk_performed']==True)])
frisk_performed_bk=len(nj_df.loc[(nj_df['frisk_performed']==True) & (nj_df['subject_race']=='black')])
frisk_performed_yt=len(nj_df.loc[(nj_df['frisk_performed']==True) & (nj_df['subject_race']=='white')])
frisk_performed_hp=len(nj_df.loc[(nj_df['frisk_performed']==True) & (nj_df['subject_race']=='hispanic')])
frisk_performed_ap=len(nj_df.loc[(nj_df['frisk_performed']==True) & (nj_df['subject_race']=='asian/pacific Islander')])
frisk_performed_ot=len(nj_df.loc[(nj_df['frisk_performed']==True) & (nj_df['subject_race']=='other') | (nj_df['subject_race']=='unknown')])

frisk_rates=[]
frisk_rates.append(frisk_performed_bk/frisk_performed)
frisk_rates.append(frisk_performed_yt/frisk_performed)
frisk_rates.append(frisk_performed_hp/frisk_performed)
frisk_rates.append(frisk_performed_ap/frisk_performed)
frisk_rates.append(frisk_performed_ot/frisk_performed)


#HIT RATES
contraband_found=len(nj_df.loc[(nj_df['contraband_found']==True)])
contraband_found_bk=len(nj_df.loc[(nj_df['contraband_found']==True) & (nj_df['subject_race']=='black')])
contraband_found_yt=len(nj_df.loc[(nj_df['contraband_found']==True) & (nj_df['subject_race']=='white')])
contraband_found_hp=len(nj_df.loc[(nj_df['contraband_found']==True) & (nj_df['subject_race']=='hispanic')])
contraband_found_ap=len(nj_df.loc[(nj_df['contraband_found']==True) & (nj_df['subject_race']=='asian/pacific Islander')])
contraband_found_ot=len(nj_df.loc[(nj_df['contraband_found']==True) & (nj_df['subject_race']=='other') | (nj_df['subject_race']=='unknown')])

hit_rates=[]
hit_rates.append(contraband_found_bk/search_conducted_bk)
hit_rates.append(contraband_found_yt/search_conducted_yt)
hit_rates.append(contraband_found_hp/search_conducted_hp)
hit_rates.append(contraband_found_ap)
hit_rates.append(contraband_found_ot/search_conducted_ot)





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
for year in num_stops_year:
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
        tmp[key]=(num_outcomes_per_year[i][key]/len(nj_df))
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
with open("/Users/hudaali/Downloads/nj_notes.txt","w+") as nj_notes:
    nj_notes.write("Minimum Sate:\n"+str(nj_min_date)+"\n")
    nj_notes.write("Maximum Date:\n"+str(nj_max_date)+"\n")
    nj_notes.write("Aproximation Population over 2009-2016:\n{}\n\n".format(aprox_nj_pop_year))
    nj_notes.write("Aproximation Population Per Race over 2009-2016:\n{}\n\n".format(aprox_pop_by_race))
    nj_notes.write("Number of Stops per Year:\n{}\n\n".format(num_stops_year))
    nj_notes.write("Rate of Stops per Year:\n{}\n\n".format(rate_stops_per_year))
    nj_notes.write("Amount of stops by race\n2009-2016:{}\n\n".format(num_stops_race))
    nj_notes.write("Number of Stops by Race per Year:\n{}\n\n".format(num_stops_race_per_year))
    nj_notes.write("STOP RATE BY RACE IN PORTPORTION TO POPULATION DEMOGRAPHIC:\n{}\n\n".format(stop_rate_race_porp_pop))
    nj_notes.write("Rate of Stops by Race:\n{}\n\n".format(rate_stops_race_per_year))
    nj_notes.write("Number of Stops by Sex per Year:\n{}\n\n".format(num_stops_sex_per_year))
    nj_notes.write("Rate of Stops by Sex per Year:\n{}\n\n".format(rate_stops_sex_per_year))
    nj_notes.write("Number of outcomes per Year:\n{}\n\n".format(num_outcomes_per_year))
    nj_notes.write("Rate of outcomes per Year:\n{}\n\n".format(rate_outcomes_per_year))
    nj_notes.write("Types of cars Stopped:\n{}\n\n".format(type_veh_colors_stopped))
    nj_notes.write("SEARCH RATES:\n{}\n\n".format(search_rates))
    nj_notes.write("FRISK RATES\n{}\n\n".format(frisk_rates))
    nj_notes.write("HIT RATES:\n{}\n\n".format(hit_rates))



tmp_bk=[]
tmp_yt=[]
tmp_hp=[]
tmp_ap=[]
tmp_ot=[]
print()
for dic in rate_stops_race_per_year:
    for key in dic.keys():
        if key=='black':
            tmp_bk.append(dic[key])
        elif key=='white':
            tmp_yt.append(dic[key])
        elif key=='hispanic':
            tmp_hp.append(dic[key])
        elif key=='asian/pacific islander':
            tmp_ap.append(dic[key])
        elif key=='other':
            tmp_ot.append(dic[key])

'''tmp=["Black","White","Hispanic","Asian/pacific Islander","Other"]
x_axis=years
y_axis=[tmp_bk,tmp_yt,tmp_hp,tmp_ap,tmp_ot]
colors=['purple','blue','brown','green','yellow']
for i in range(len(y_axis)):
    plt.plot(x_axis, y_axis[i],label=tmp[i],color=colors[i],marker='o')

plt.title('Rate of Traffic Stops by Race per Year')
plt.xlabel('Years')
plt.ylabel('Rate of Stops')
plt.legend()
plt.show()'''
tmp_bk=[]
tmp_yt=[]
tmp_hp=[]
tmp_ap=[]
tmp_ot=[]

'''tmp_ma=[]
tmp_fem=[]


for dic in rate_stops_sex_per_year:
    for key in dic.keys():
        if key=='male':
            tmp_ma.append(dic[key])
        elif key=='female':
            tmp_fem.append(dic[key])
        else:
            tmp_ot.append(dic[key])
            
print(tmp_ma)
print(tmp_fem)
print(tmp_ot)

        

tmp=["Male","Female","Other"]
x_axis=years
y_axis=[tmp_ma,tmp_fem,tmp_ot]
colors=['purple','blue','brown']
for i in range(len(y_axis)):
    plt.plot(x_axis, y_axis[i],label=tmp[i],color=colors[i],marker='o')
plt.title('Rate of Traffic Stops by Sex per Year')
plt.xlabel('Years')
plt.ylabel('Rate of Stops')
plt.legend()
plt.show() '''




   
    
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



