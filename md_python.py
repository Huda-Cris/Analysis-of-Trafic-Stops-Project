import csv
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


with open ("/Users/hudaali/Downloads/md_statewide_2020_04_01.csv", "r+") as md_csv:
    md=pd.read_csv(md_csv)
    old_md_df=pd.DataFrame(md)

old_md_df['date'] = pd.to_datetime(old_md_df['date'], format='%Y-%m-%d')
md_df = old_md_df[['date','time','department_name','type','subject_age','subject_race', 'subject_sex','violation','arrest_made','outcome','contraband_found','search_conducted','search_person','search_vehicle','reason_for_stop','reason_for_search','reason_for_arrest']]
md_df=md_df.loc[(md_df['date'] >= '2007-01-01') & (md_df['date'] <= '2013-12-31') & (md_df['type']=='vehicular')] #filtered data file
md_max_date=md_df['date'].max()#2014-03-31 00:00:00
md_min_date=md_df['date'].min()#2007-01-01 00:00:00


# Aprox population 
aprox_md_pop_year=[5653408,5730388,5737000,5785000,5834000]
aprox_pop_by_race={
    'black':[],
    'white':[],
    'hispanic':[],
    'asian/pacific Islander':[],
    'other':[]
    }
for pop in aprox_md_pop_year:
    for key in aprox_pop_by_race:
        if key=='black':
            aprox_pop_by_race[key].append(0.2901*pop)
        elif key=='white':
            aprox_pop_by_race[key].append(pop*0.55)
        elif key=='hispanic':
            aprox_pop_by_race[key].append(0.0805*pop)
        elif key=='asian/pacific Islander':
            aprox_pop_by_race[key].append(pop*0.056)
        elif key=='other':
            aprox_pop_by_race[key].append(pop*0.0544)
years=["2007","2009","2011","2012","2013"]
# NUMBER OF STOPS PER YEAR

num_of_stops_2007=md_df.query('20070101 <= date <20080101')
num_of_stops_2008=md_df.query('20080101 <= date <20090101')
num_of_stops_2009=md_df.query('20090101 <= date <20100101')
num_of_stops_2010=md_df.query('20100101 <= date <20110101')
num_of_stops_2011=md_df.query('20110101 <= date <20120101')
num_of_stops_2012=md_df.query('20120101 <= date <20130101')
num_of_stops_2013=md_df.query('20130101 <= date <20140101')



num_stops_year=[num_of_stops_2007,num_of_stops_2009,num_of_stops_2011,num_of_stops_2012,num_of_stops_2013]

#  RATE OF STOPS  PER YEAR
rate_stops_per_year=[]

for i in range (len(aprox_md_pop_year)):
    rate_stops_per_year.append(len(num_stops_year[i])/aprox_md_pop_year[i])

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
        tmp[key]=(num_stops_race_per_year[i][key]/len(md_df))
    rate_stops_race_per_year.append(tmp)

#STOP RATE IN PORTPORTION TO POP RACE 
num_bk_stopped=len(md_df.loc[md_df['subject_race']=='black'])
num_yt_stopped=len(md_df.loc[md_df['subject_race']=='white'])
num_hp_stopped=len(md_df.loc[md_df['subject_race']=='hispanic'])
num_ap_stopped=len(md_df.loc[md_df['subject_race']=='asian/pacific Islander'])
num_ot_stopped=len(md_df.loc[md_df['subject_race']=='other'])
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
        tmp[key]=(num_stops_sex_per_year[i][key]/len(md_df))
    rate_stops_sex_per_year.append(tmp)

#SEARCH  RATE

search_conducted=len(md_df.loc[(md_df['search_conducted']==True)])
search_conducted_bk=len(md_df.loc[(md_df['search_conducted']==True) & (md_df['subject_race']=='black')])
search_conducted_yt=len(md_df.loc[(md_df['search_conducted']==True) & (md_df['subject_race']=='white')])
search_conducted_hp=len(md_df.loc[(md_df['search_conducted']==True) & (md_df['subject_race']=='hispanic')])
search_conducted_ap=len(md_df.loc[(md_df['search_conducted']==True) & (md_df['subject_race']=='asian/pacific Islander')])
search_conducted_ot=len(md_df.loc[(md_df['search_conducted']==True) & (md_df['subject_race']=='other') | (md_df['subject_race']=='unknown')])

search_rates=[]
search_rates.append(search_conducted_bk/search_conducted)
search_rates.append(search_conducted_yt/search_conducted)
search_rates.append(search_conducted_hp/search_conducted)
search_rates.append(search_conducted_ap/search_conducted)
search_rates.append(search_conducted_ot/search_conducted)

#HIT RATES
contraband_found=len(md_df.loc[(md_df['contraband_found']==True)])
contraband_found_bk=len(md_df.loc[(md_df['contraband_found']==True) & (md_df['subject_race']=='black')])
contraband_found_yt=len(md_df.loc[(md_df['contraband_found']==True) & (md_df['subject_race']=='white')])
contraband_found_hp=len(md_df.loc[(md_df['contraband_found']==True) & (md_df['subject_race']=='hispanic')])
contraband_found_ap=len(md_df.loc[(md_df['contraband_found']==True) & (md_df['subject_race']=='asian/pacific Islander')])
contraband_found_ot=len(md_df.loc[(md_df['contraband_found']==True) & (md_df['subject_race']=='other') | (md_df['subject_race']=='unknown')])

hit_rates=[]
hit_rates.append(contraband_found_bk/search_conducted_bk)
hit_rates.append(contraband_found_yt/search_conducted_yt)
hit_rates.append(contraband_found_hp/search_conducted_hp)
hit_rates.append(contraband_found_ap)
hit_rates.append(contraband_found_ot/search_conducted_ot)

white_hit_rate_filter=md_df.loc[(md_df['search_conducted']==True) & (md_df['subject_race']=='white')]
white_hit_rate=white_hit_rate_filter.groupby(['subject_race','department_name'])['contraband_found'].mean()

minority_hit_filter=md_df.loc[(md_df['search_conducted']==True) & (md_df['subject_race']=='black')|(md_df['subject_race']=='hispanic')]
minority_hit_rate=(minority_hit_filter.groupby(['subject_race','department_name'])['contraband_found']).mean()

tmp_filter=md_df.loc[(md_df['subject_race']=='white')]
num_searches_district=md_df.groupby(['department_name'])['search_conducted'].count()

reason_stop_sex=old_md_df.groupby(['subject_sex','reason_for_stop']).search_conducted.mean()
condition = old_md_df.subject_sex.isin(["female", "male"]) & old_md_df.reason_for_stop

search_type_by_sex = (old_md_df[condition].
  groupby("subject_sex").reason_for_stop.value_counts(normalize = True).unstack()
)
# condition = old_md_df.subject_race.isin(["white", "black", "hispanic", "asian"]) & old_md_df.violation
reason_stop_race=old_md_df.groupby(['subject_race','violation']).search_conducted.max()
print(reason_stop_race)
# search_type_by_race = (old_md_df[condition].
#   groupby("subject_race").violation.value_counts(normalize = True).unstack()
# )
# search_type_by_race.plot(kind='bar')
# plt.title("Proportion of common search types across 4 races")
# plt.ylabel("Average Number of reasons")
# plt.show()

with open("/Users/hudaali/Downloads/md_notes.txt",'w+') as md_notes:
    md_notes.write("MINIMUM DATE:\n{}\n\n".format(md_min_date))
    md_notes.write("MAXIMUM DATE:\n{}\n\n".format(md_max_date))
    md_notes.write("APROXIMATION POPLUATION PER YEAR:\n{}\n\n".format(aprox_md_pop_year))
    md_notes.write("APROXIMATION POPLUATION PER RACE PER YEAR:\n{}\n\n".format(aprox_pop_by_race))
    md_notes.write("NUMBER OF STOPS PER RACE PER YEAR:\n{}\n\n".format(num_stops_race_per_year))
    md_notes.write("RATE OF STOPS PER RACE PER YEAR:\n{}\n\n".format(rate_stops_race_per_year))
    md_notes.write("STOP RATE BY RACE IN PORTPORTION TO POPULATION DEMOGRAPHIC:\n{}\n\n".format(stop_rate_race_porp_pop))
    md_notes.write("NUMBER OF STOPS PER SEX PER YEAR:\n{}\n\n".format(num_stops_sex_per_year))
    md_notes.write("RATE OF STOPS PER SEX PER YEAR:\n{}\n\n".format(rate_stops_sex_per_year))
    md_notes.write("SEARCH RATES:\n{}\n\n".format(search_rates))
    md_notes.write("HIT RATES:\n{}\n\n".format(hit_rates))


'''#METHODS TO GET LOCATIONS
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
'''

'''tmp_bk=[]
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
            tmp_ot.append(dic[key])'''

'''tmp_bk=stop_rate_race_porp_pop['black']
tmp_yt=stop_rate_race_porp_pop['white']
tmp_hp=stop_rate_race_porp_pop['hispanic']
tmp_ap=stop_rate_race_porp_pop['asian/pacific Islander']
tmp_ot=stop_rate_race_porp_pop['other']

tmp=["Black","White","Hispanic","Asian/pacific Islander","Other"]
x_axis=years
y_axis=[tmp_bk,tmp_yt,tmp_hp,tmp_ap,tmp_ot]
colors=['purple','blue','brown','green','yellow']
for i in range(len(y_axis)):
    plt.plot(x_axis, y_axis[i],label=tmp[i],color=colors[i],marker='o')

plt.title('Rate of Traffic Stops by Race per Year in Porportion of Demographic Population Size')
plt.xlabel('Years')
plt.ylabel('Rate of Stops')
plt.legend()
plt.show()'''

'''tmp_ma=[]
tmp_fem=[]
tmp_ot=[]

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


x_axis=years
y_axis=rate_stops_per_year

#MARYLAND STOP RATE

# plt.bar(x_axis,y_axis,color='brown')
# plt.title("Rate of Traffic Stops Maryland 2007-2013")
# plt.xlabel("Years")
# plt.ylabel("Rate of Stops")
# plt.ylim(ymin=0)
# plt.show()