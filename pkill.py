from re import S
import xlrd
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import openpyxl

path="/Users/hudaali/Downloads/MPVDatasetDownload.xlsx"
df_0=pd.read_excel(path,sheet_name=0)
df_0=pd.DataFrame(df_0)
columns=df_0.columns
condition= df_0.State.isin(['MD','PA','NJ','RI'])
df_0.rename(columns = {'Encounter Type (DRAFT)':'encounter_type','Date of Incident (month/day/year)':'Date','Victim\'s race': 'subject_race'}, inplace=True)
condition= df_0.State.isin(['MD','PA','NJ','RI']) & (df_0.encounter_type.isin(['Traffic Stop']) |df_0.encounter_type.isin(['Traffic Stop/Other Non-Violent Offense']) | df_0.encounter_type.isin(['Part 1 Violent Crime/Traffic Stop']) | df_0.encounter_type.isin(['Other Non-Violent Offense']))
kils_by_state=df_0[condition].groupby(['State']).count()
kils_by_state_graph = (df_0[condition].
  groupby("State").encounter_type.value_counts(normalize = True).unstack()
)
kills_by_state_race_graph = (df_0[condition].
  groupby(["State"]).subject_race.value_counts(normalize = True).unstack()
)
print(df_0[condition].groupby(["State",'subject_race']).encounter_type.count())

path="/Users/hudaali/Downloads/MPVDatasetDownload.xlsx"
df_1=pd.read_excel(path,sheet_name=1)
df_1=pd.DataFrame(df_1)
columns=df_1.columns
df_1.rename(columns = {'All People Killed by Police (1/1/2013-12/31/2021)':'all_ppl_killed', 'Black People Killed by Police (1/1/2013-12/31/2021)': 'bk_killed'}, inplace=True)

condition= df_1.State.isin(['Maryland','Pennsylvania','New Jersey','Rhode Island'])
print(df_1[condition].groupby(['State','all_ppl_killed','bk_killed']).count())
ppl_killed_stat={'MD': 38, 'NJ': 20, 'PA':53}



# kills_by_state_race_graph.plot(kind='bar')
# plt.title("Porportion of Fatalities per State per Race")
# plt.ylabel("Rate of Fatalities")
# plt.show()
