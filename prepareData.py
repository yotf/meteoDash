import os
import pandas as pd
import numpy as np

csv_fnames = [d for d in os.listdir(".") if d.startswith("00000")]

min_date = pd.datetime(year=2019,month=4,day=1)
max_date = pd.datetime(year=2000,month=1,day=1)
for fname in csv_fnames:
    df = pd.read_csv(fname,usecols=[0,1],index_col="Date",converters={"Date":pd.to_datetime})
    df.columns = ["Tavg"]
    print (min_date)
    print (df.index[0])
    min_date = df.index[0] if df.index[0] < min_date else min_date
    max_date = df.index[-1] if df.index[-1] > max_date else max_date

for fname in csv_fnames:
    df = pd.read_csv(fname,usecols=[0,1],index_col="Date",converters={"Date":pd.to_datetime})
    df.columns = ["Tavg"]
    df = df.resample('2H').mean()
    df.to_csv(fname)
