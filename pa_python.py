import csv
from turtle import xcor
from matplotlib import markers
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


with open ("/Users/hudaali/Downloads/pa_philadelphia_2020_04_01.csv", "r+") as pa_csv:
    pa=pd.read_csv(pa_csv)
    old_pa_df=pd.DataFrame(pa)

old_pa_df['date'] = pd.to_datetime(old_pa_df['date'], format='%Y-%m-%d')


pa_df = old_pa_df[['date','time','location','district','subject_age','subject_race', 'subject_sex','arrest_made','outcome','contraband_found','frisk_performed','search_person','search_vehicle','type','search_conducted']]

pa_df=pa_df.loc[(pa_df['date'] >= '2014-01-01') & (pa_df['date'] <= '2017-12-31') & (pa_df['type']=='vehicular')] #filtered data file
pa_max_date=pa_df['date'].max()#2018-04-14 00:00:00
pa_min_date=pa_df['date'].min()#2014-01-01 00:00:00

#Aprox population 
aprox_pa_pop_year=[6046380,6056820,6066660,6078520]
aprox_pop_by_race={
    'black':[],
    'white':[],
    'hispanic':[],
    'asian/pacific Islander':[],
    'other':[]
    }
for pop in aprox_pa_pop_year:
    for key in aprox_pop_by_race:
        if key=='black':
            aprox_pop_by_race[key].append(0.4135*pop)
        elif key=='white':
            aprox_pop_by_race[key].append(pop*0.345)
        elif key=='hispanic':
            aprox_pop_by_race[key].append(0.143*pop)
        elif key=='asian/pacific Islander':
            aprox_pop_by_race[key].append(pop*0.072)
        elif key=='other':
            aprox_pop_by_race[key].append(pop*0.0265)




years=['2014','2015','2016','2017']

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


#NUMBER OD STOPS PER RACE
num_stops_race={}
for stop in pa_df['subject_race']:
    if stop in num_stops_race:
        num_stops_race[stop]+=1
    else:
        num_stops_race[stop]=1


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
        tmp[key]=(num_stops_race_per_year[i][key]/len(pa_df))
    rate_stops_race_per_year.append(tmp)



#STOP RATE IN PORTPORTION TO POP RACE 
num_bk_stopped=len(pa_df.loc[pa_df['subject_race']=='black'])
num_yt_stopped=len(pa_df.loc[pa_df['subject_race']=='white'])
num_hp_stopped=len(pa_df.loc[pa_df['subject_race']=='hispanic'])
num_ap_stopped=len(pa_df.loc[pa_df['subject_race']=='asian/pacific Islander'])
num_ot_stopped=len(pa_df.loc[pa_df['subject_race']=='other'])
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

# RATE OF STOPS PER RACE PER YEAR
rate_stops_sex_per_year=[]
for i in range(len(num_stops_sex_per_year)):
    tmp={}
    for key in num_stops_sex_per_year[i].keys():
        tmp[key]=(num_stops_sex_per_year[i][key]/len(pa_df))
    rate_stops_sex_per_year.append(tmp)

#SEARCH  RATE
search_conducted=len(pa_df.loc[(pa_df['search_conducted']==True)])
search_conducted_bk=len(pa_df.loc[(pa_df['search_conducted']==True) & (pa_df['subject_race']=='black')])
search_conducted_yt=len(pa_df.loc[(pa_df['search_conducted']==True) & (pa_df['subject_race']=='white')])
search_conducted_hp=len(pa_df.loc[(pa_df['search_conducted']==True) & (pa_df['subject_race']=='hispanic')])
search_conducted_ap=len(pa_df.loc[(pa_df['search_conducted']==True) & (pa_df['subject_race']=='asian/pacific Islander')])
search_conducted_ot=len(pa_df.loc[(pa_df['search_conducted']==True) & (pa_df['subject_race']=='other') | (pa_df['subject_race']=='unknown')])

search_rates=[]
search_rates.append(search_conducted_bk/search_conducted)
search_rates.append(search_conducted_yt/search_conducted)
search_rates.append(search_conducted_hp/search_conducted)
search_rates.append(search_conducted_ap/search_conducted)
search_rates.append(search_conducted_ot/search_conducted)


#Frisk Rate

frisk_performed=len(pa_df.loc[(pa_df['frisk_performed']==True)])
frisk_performed_bk=len(pa_df.loc[(pa_df['frisk_performed']==True) & (pa_df['subject_race']=='black')])
frisk_performed_yt=len(pa_df.loc[(pa_df['frisk_performed']==True) & (pa_df['subject_race']=='white')])
frisk_performed_hp=len(pa_df.loc[(pa_df['frisk_performed']==True) & (pa_df['subject_race']=='hispanic')])
frisk_performed_ap=len(pa_df.loc[(pa_df['frisk_performed']==True) & (pa_df['subject_race']=='asian/pacific Islander')])
frisk_performed_ot=len(pa_df.loc[(pa_df['frisk_performed']==True) & (pa_df['subject_race']=='other') | (pa_df['subject_race']=='unknown')])

frisk_rates=[]
frisk_rates.append(frisk_performed_bk/frisk_performed)
frisk_rates.append(frisk_performed_yt/frisk_performed)
frisk_rates.append(frisk_performed_hp/frisk_performed)
frisk_rates.append(frisk_performed_ap/frisk_performed)
frisk_rates.append(frisk_performed_ot/frisk_performed)


#HIT RATES
contraband_found=len(pa_df.loc[(pa_df['contraband_found']==True)])
contraband_found_bk=len(pa_df.loc[(pa_df['contraband_found']==True) & (pa_df['subject_race']=='black')])
contraband_found_yt=len(pa_df.loc[(pa_df['contraband_found']==True) & (pa_df['subject_race']=='white')])
contraband_found_hp=len(pa_df.loc[(pa_df['contraband_found']==True) & (pa_df['subject_race']=='hispanic')])
contraband_found_ap=len(pa_df.loc[(pa_df['contraband_found']==True) & (pa_df['subject_race']=='asian/pacific Islander')])
contraband_found_ot=len(pa_df.loc[(pa_df['contraband_found']==True) & (pa_df['subject_race']=='other') | (pa_df['subject_race']=='unknown')])

hit_rates=[]
hit_rates.append(contraband_found_bk/search_conducted_bk)
hit_rates.append(contraband_found_yt/search_conducted_yt)
hit_rates.append(contraband_found_hp/search_conducted_hp)
hit_rates.append(contraband_found_ap)
hit_rates.append(contraband_found_ot/search_conducted_ot)

#hite rate = contraband found/ search conducted
#Find rate of contraband found per race per district
#Find search rates per per per district
p_tmp=pa_df.loc[(pa_df['search_conducted']==True)]
hit_rate=p_tmp.groupby(['subject_race','district'])['contraband_found'].mean()


white_hit_rate_filter=pa_df.loc[(pa_df['search_conducted']==True) & (pa_df['subject_race']=='white')]
white_hit_rate=white_hit_rate_filter.groupby(['subject_race','district']).contraband_found.mean()

minority_hit_filter=pa_df.loc[(pa_df['search_conducted']==True) & (pa_df['subject_race']=='black')|(pa_df['subject_race']=='hispanic')]
minority_hit_rate=(minority_hit_filter.groupby(['subject_race','district']).contraband_found.mean())

tmp_filter=pa_df.loc[(pa_df['subject_race']=='white')]
num_searches_district=pa_df.groupby(['district'])['search_conducted'].count()

for i in range(len(white_hit_rate)):
    white_hit_rate[i]=white_hit_rate[i]*100
for i in range(len(minority_hit_rate)):
    minority_hit_rate[i]=minority_hit_rate[i]*100

'''plt.scatter(white_hit_rate, minority_hit_rate['black'], facecolors='none', edgecolors='black')
z = np.polyfit(white_hit_rate, minority_hit_rate['black'], 1)
p = np.poly1d(z)
plt.plot(white_hit_rate, p(white_hit_rate),color='brown',linestyle='--',linewidth=1)
plt.title('Minority Hit Rates v. White Hit Rates')
plt.xlabel('White Hit Rates')
plt.ylabel('Minority Hit Rates-BLACK')
plt.ylim(0,80)
plt.xlim(0,80)
plt.legend(loc='best')
plt.show()

plt.scatter(white_hit_rate, minority_hit_rate['hispanic'],facecolors='none', edgecolors='b')
z = np.polyfit(white_hit_rate, minority_hit_rate['hispanic'], 1)
p = np.poly1d(z)
plt.plot(white_hit_rate, p(white_hit_rate),color='brown',linestyle='--',linewidth=1)
plt.title('Minority Hit Rates v. White Hit Rates')
plt.xlabel('White Hit Rates')
plt.ylabel('Minority Hit Rates-HISPANIC')
plt.ylim(0,80)
plt.xlim(0,80)
plt.show()'''

# NUMBER OF TIMES VEICLES WERE SEARCHED
veh_search={}
for search in pa_df['search_vehicle']:
    if search in veh_search:
        veh_search[search]+=1
    else:
        veh_search[search]=1


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
print(pa_df)

with open("/Users/hudaali/Downloads/pa_notes.txt",'w+') as pa_notes:
    pa_notes.write("MINIMUM DATE:\n{}\n\n".format(pa_min_date))
    pa_notes.write("MAXIMUM DATE:\n{}\n\n".format(pa_max_date))
    pa_notes.write("APROXIMATION POPLUATION PER YEAR:\n{}\n\n".format(aprox_pa_pop_year))
    pa_notes.write("APROXIMATION POPLUATION PER RACE PER YEAR:\n{}\n\n".format(aprox_pop_by_race))
    pa_notes.write("NUMBER OF STOPS PER RACE PER YEAR:\n{}\n\n".format(num_stops_race_per_year))
    pa_notes.write("RATE OF STOPS PER RACE PER YEAR:\n{}\n\n".format(rate_stops_race_per_year))
    pa_notes.write("STOP RATE BY RACE IN PORTPORTION TO POPULATION DEMOGRAPHIC:\n{}\n\n".format(stop_rate_race_porp_pop))
    pa_notes.write("NUMBER OF STOPS PER SEX PER YEAR:\n{}\n\n".format(num_stops_sex_per_year))
    pa_notes.write("RATE OF STOPS PER SEX PER YEAR:\n{}\n\n".format(rate_stops_sex_per_year))
    pa_notes.write("SEARCH RATES:\n{}\n\n".format(search_rates))
    pa_notes.write("FRISK RATES\n{}\n\n".format(frisk_rates))
    pa_notes.write("HIT RATES:\n{}\n\n".format(hit_rates))
    pa_notes.write("WHITE HIT RATES BY DISTRICT:\n{}\n\n".format(white_hit_rate))
    pa_notes.write("MINORITY (BLACK AND HISPANIC) HIT RATES BY DISTRICT:\n{}\n\n".format(minority_hit_rate))
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


tmp_bk=stop_rate_race_porp_pop['black']
tmp_yt=stop_rate_race_porp_pop['white']
tmp_hp=stop_rate_race_porp_pop['hispanic']
tmp_ap=stop_rate_race_porp_pop['asian/pacific Islander']
tmp_ot=stop_rate_race_porp_pop['other']

'''for dic in num_stops_race_per_year:
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



# tmp=["Black","White","Hispanic","Asian/pacific Islander","Other"]
# x_axis=years
# y_axis=[tmp_bk,tmp_yt,tmp_hp,tmp_ap,tmp_ot]
# colors=['purple','blue','brown','green','yellow']
# for i in range(len(y_axis)):
#     plt.plot(x_axis, y_axis[i],label=tmp[i],color=colors[i],marker='o')

# plt.title('Rate of Traffic Stops by Race per Year in Porportion of Demographic Population Size')
# plt.xlabel('Years')
# plt.ylabel('Rate of Stops')
# plt.legend()
# plt.show()