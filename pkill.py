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
df=pd.read_excel(path,sheet_name=1)
df=pd.DataFrame(df)
print(df.head())