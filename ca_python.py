import csv
import pandas as pd
import glob
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp



ct_files=os.path.join("/Users/hudaali/Downloads/cd_data_sets/connecticut-r*.csv")



ct_files=glob.glob(ct_files)   

print("Resultant CSV after joining all CSV files at a particular location...")

# joining files with concat and read_csv
ct_df = pd.concat(map(pd.read_csv, ct_files), ignore_index=True)
ct_df=pd.DataFrame(ct_df)

ct_df['InterventionDateTime'] = pd.to_datetime(ct_df['InterventionDateTime']).dt.strftime('%Y-%m-%d %H:%M:%S')
ca_max_date=ct_df['InterventionDateTime'].max()
ca_min_date=ct_df['InterventionDateTime'].min()
print(ca_max_date)
print(ca_min_date)

ca_df = ct_df[['InterventionDateTime','SubjectRaceCode', 'SubjectSexCode','InterventionLocationName','ReasonForStop','CustodialArrestIndicator','VehicleSearchedIndicator','SubjectAge']]



def ct_stopsPerLoc():
    locations={}
    for twp in ct_df['InterventionLocationName']:
        twp=(str(twp)).lower()
        twp=twp.strip()
        if twp in locations:
            locations[twp]+=1
        else:
            locations[twp]=1

    with open("/Users/hudaali/Desktop/Dict.txt",'w+') as dict:
        for key in locations.items():
            dict.write(str(key))

ct_stopsPerLoc()

