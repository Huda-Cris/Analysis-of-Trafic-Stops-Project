import csv
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


with open ("/Users/hudaali/Downloads/ri_statewide_2020_04_01.csv", "r+") as ri_csv:
    ri=pd.read_csv(ri_csv)
    old_ri_df=pd.DataFrame(ri)

old_ri_df['date'] = pd.to_datetime(old_ri_df['date'], format='%Y-%m-%d')

#print(old_ri_df['type'])
ri_df = old_ri_df[['date','time','subject_race', 'subject_sex','arrest_made','outcome','contraband_found','frisk_performed','search_conducted','reason_for_search','reason_for_stop','type']]


ri_max_date=ri_df['date'].max()#2015-12-31 00:00:00
ri_min_date=ri_df['date'].min()#2005-01-02 00:00:00

# Aprox population 
aprox_ri_pop_year=[1067916,1063096,1057315,1055003,1053646,1052567,1054000,1052000,1052000,1052000,1053000]
aprox_pop_by_race={
    'black':[],
    'white':[],
    'hispanic':[],
    'asian/pacific Islander':[],
    'other':[]
    }
for pop in aprox_ri_pop_year:
    for key in aprox_pop_by_race:
        if key=='black':
            aprox_pop_by_race[key].append(0.0535*pop)
        elif key=='white':
            aprox_pop_by_race[key].append(pop*0.767)
        elif key=='hispanic':
            aprox_pop_by_race[key].append(0.1265*pop)
        elif key=='asian/pacific Islander':
            aprox_pop_by_race[key].append(pop*0.0305)
        elif key=='other':
            aprox_pop_by_race[key].append(pop*0.025)
years=["2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015"]

# NUMBER OF STOPS PER YEAR
num_of_stops_2005=ri_df.query('20050101 <= date <20060101')
num_of_stops_2006=ri_df.query('20060101 <= date <20070101')
num_of_stops_2007=ri_df.query('20070101 <= date <20080101')
num_of_stops_2008=ri_df.query('20080101 <= date <20090101')
num_of_stops_2009=ri_df.query('20090101 <= date <20100101')
num_of_stops_2010=ri_df.query('20100101 <= date <20110101')
num_of_stops_2011=ri_df.query('20110101 <= date <20120101')
num_of_stops_2012=ri_df.query('20120101 <= date <20130101')
num_of_stops_2013=ri_df.query('20130101 <= date <20140101')
num_of_stops_2014=ri_df.query('20140101 <= date <20150101')
num_of_stops_2015=ri_df.query('20150101 <= date <20160101')


num_stops_year=[num_of_stops_2005,num_of_stops_2006,num_of_stops_2007,num_of_stops_2008,num_of_stops_2009,num_of_stops_2010,num_of_stops_2011,num_of_stops_2012,num_of_stops_2013,num_of_stops_2014,num_of_stops_2015]

#  RATE OF STOPS  PER YEAR
rate_stops_per_year=[]

for i in range (len(aprox_ri_pop_year)):
    rate_stops_per_year.append(len(num_stops_year[i])/aprox_ri_pop_year[i])

# NUMBER OF STOPS PER RACE PER YEAR
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
        tmp[key]=(num_stops_race_per_year[i][key]/len(ri_df))
    rate_stops_race_per_year.append(tmp)

#STOP RATE IN PORTPORTION TO POP RACE 
num_bk_stopped=len(ri_df.loc[ri_df['subject_race']=='black'])
num_yt_stopped=len(ri_df.loc[ri_df['subject_race']=='white'])
num_hp_stopped=len(ri_df.loc[ri_df['subject_race']=='hispanic'])
num_ap_stopped=len(ri_df.loc[ri_df['subject_race']=='asian/pacific Islander'])
num_ot_stopped=len(ri_df.loc[ri_df['subject_race']=='other'])
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

# RATE OF STOPS PER SEX PER YEAR
rate_stops_sex_per_year=[]
for i in range(len(num_stops_sex_per_year)):
    tmp={}
    for key in num_stops_sex_per_year[i].keys():
        tmp[key]=(num_stops_sex_per_year[i][key]/len(ri_df))
    rate_stops_sex_per_year.append(tmp)

#SEARCH  RATE

search_conducted=len(ri_df.loc[(ri_df['search_conducted']==True)])
search_conducted_bk=len(ri_df.loc[(ri_df['search_conducted']==True) & (ri_df['subject_race']=='black')])
search_conducted_yt=len(ri_df.loc[(ri_df['search_conducted']==True) & (ri_df['subject_race']=='white')])
search_conducted_hp=len(ri_df.loc[(ri_df['search_conducted']==True) & (ri_df['subject_race']=='hispanic')])
search_conducted_ap=len(ri_df.loc[(ri_df['search_conducted']==True) & (ri_df['subject_race']=='asian/pacific Islander')])
search_conducted_ot=len(ri_df.loc[(ri_df['search_conducted']==True) & (ri_df['subject_race']=='other') | (ri_df['subject_race']=='unknown')])

search_rates=[]
search_rates.append(search_conducted_bk/search_conducted)
search_rates.append(search_conducted_yt/search_conducted)
search_rates.append(search_conducted_hp/search_conducted)
search_rates.append(search_conducted_ap/search_conducted)
search_rates.append(search_conducted_ot/search_conducted)
print(search_rates)

#Frisk Rate

frisk_performed=len(ri_df.loc[(ri_df['frisk_performed']==True)])
frisk_performed_bk=len(ri_df.loc[(ri_df['frisk_performed']==True) & (ri_df['subject_race']=='black')])
frisk_performed_yt=len(ri_df.loc[(ri_df['frisk_performed']==True) & (ri_df['subject_race']=='white')])
frisk_performed_hp=len(ri_df.loc[(ri_df['frisk_performed']==True) & (ri_df['subject_race']=='hispanic')])
frisk_performed_ap=len(ri_df.loc[(ri_df['frisk_performed']==True) & (ri_df['subject_race']=='asian/pacific Islander')])
frisk_performed_ot=len(ri_df.loc[(ri_df['frisk_performed']==True) & (ri_df['subject_race']=='other') | (ri_df['subject_race']=='unknown')])

frisk_rates=[]
frisk_rates.append(frisk_performed_bk/frisk_performed)
frisk_rates.append(frisk_performed_yt/frisk_performed)
frisk_rates.append(frisk_performed_hp/frisk_performed)
frisk_rates.append(frisk_performed_ap/frisk_performed)
frisk_rates.append(frisk_performed_ot/frisk_performed)
print(frisk_rates)

#HIT RATES
contraband_found=len(ri_df.loc[(ri_df['contraband_found']==True)])
contraband_found_bk=len(ri_df.loc[(ri_df['contraband_found']==True) & (ri_df['subject_race']=='black')])
contraband_found_yt=len(ri_df.loc[(ri_df['contraband_found']==True) & (ri_df['subject_race']=='white')])
contraband_found_hp=len(ri_df.loc[(ri_df['contraband_found']==True) & (ri_df['subject_race']=='hispanic')])
contraband_found_ap=len(ri_df.loc[(ri_df['contraband_found']==True) & (ri_df['subject_race']=='asian/pacific Islander')])
contraband_found_ot=len(ri_df.loc[(ri_df['contraband_found']==True) & (ri_df['subject_race']=='other') | (ri_df['subject_race']=='unknown')])

hit_rates=[]
hit_rates.append(contraband_found_bk/search_conducted_bk)
hit_rates.append(contraband_found_yt/search_conducted_yt)
hit_rates.append(contraband_found_hp/search_conducted_hp)
hit_rates.append(contraband_found_ap)
hit_rates.append(contraband_found_ot/search_conducted_ot)
print(hit_rates)

# TYPES OF REASONS OF STOP
reasons_search={}

for rea in ri_df['reason_for_stop']:
    if rea in reasons_search:
        reasons_search[rea]+=1
    else:
        reasons_search[rea]=1

# REASONS FOR SEARCH OVER THE YEARS
reasons_search_years=[]

for year in num_stops_year:
    tmp={}
    for reason in year['reason_for_stop']:
        if reason in tmp:
            tmp[reason]+=1
        else:
            tmp[reason]=1
    reasons_search_years.append(tmp)


# Number OF OUTCOMES 
num_outcomes={}
for oc in ri_df['outcome']:
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
        tmp[key]=(num_outcomes_per_year[i][key]/len(ri_df))
    rate_outcomes_per_year.append(tmp)

'''with open("/Users/hudaali/Downloads/ri_notes.txt",'w+') as ri_notes:
    ri_notes.write("MINIMUM DATE:\n{}\n\n".format(ri_min_date))
    ri_notes.write("MAXIMUM DATE:\n{}\n\n".format(ri_max_date))
    ri_notes.write("APROXIMATION POPLUATION PER YEAR:\n{}\n\n".format(aprox_ri_pop_year))
    ri_notes.write("APROXIMATION POPLUATION PER RACE PER YEAR:\n{}\n\n".format(aprox_pop_by_race))
    ri_notes.write("NUMBER OF STOPS PER RACE PER YEAR:\n{}\n\n".format(num_stops_race_per_year))
    ri_notes.write("RATE OF STOPS PER RACE PER YEAR:\n{}\n\n".format(rate_stops_race_per_year))
    ri_notes.write("STOP RATE BY RACE IN PORTPORTION TO POPULATION DEMOGRAPHIC:\n{}\n\n".format(stop_rate_race_porp_pop))
    ri_notes.write("NUMBER OF STOPS PER SEX PER YEAR:\n{}\n\n".format(num_stops_sex_per_year))
    ri_notes.write("RATE OF STOPS PER SEX PER YEAR:\n{}\n\n".format(rate_stops_sex_per_year))'''
    

'''tmp_bk=[]
tmp_yt=[]
tmp_hp=[]
tmp_ap=[]
tmp_ot=[]
print()
for dic in num_stops_race_per_year:
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



tmp=["Black","White","Hispanic","Asian/pacific Islander","Other"]
x_axis=years
y_axis=[tmp_bk,tmp_yt,tmp_hp,tmp_ap,tmp_ot]
colors=['purple','blue','brown','green','yellow']
for i in range(len(y_axis)):
    plt.plot(x_axis, y_axis[i],label=tmp[i],color=colors[i],marker='o')

plt.title('Number of Traffic Stops by Race per Year')
plt.xlabel('Years')
plt.ylabel('Number of Stops')
plt.legend()
plt.show()'''


