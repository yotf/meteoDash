import os
import pandas as pd
import numpy as np
from metpy.calc import thermo
from metpy.units import units

csv_fnames = [d for d in os.listdir("./CSV") if d.startswith("0000") and d.endswith("00.csv")]

def make_daily_avgs(hourly_df):
    mindf = hourly_df.Tavg.resample('D').min()
    maxdf = hourly_df.Tavg.resample('D').max()
    zz = pd.concat([mindf,maxdf],axis=1)
    zz.columns = ["Tmin","Tmax"]
    df = pd.concat([hourly_df.resample('D').mean(),zz],axis=1)
    Lv = 2265.705
    Cp = 1.003
    df["tendt"] = Cp*df.Tavg.diff()/(24*3600)
    df["tendq"] = Lv*df.q.diff()/(24*3600)
    df["bowen"] = (Cp*df.Tavg.diff())/(Lv*df.q.diff())
    df.bowen[(df.bowen>5) | (df.bowen<-5)]=None
    E_tmin = df.Tmin.apply(lambda x: thermo.saturation_vapor_pressure(x * units.celsius))
    E_tmax = df.Tmax.apply(lambda x: thermo.saturation_vapor_pressure(x* units.celsius))
    E_avg = df.Tavg.apply(lambda x: thermo.saturation_vapor_pressure(x* units.celsius))
    df["R2"] = (E_tmin/E_tmax).apply(lambda x: x.magnitude)
    df["R1"] =  ((df.RH*E_avg)/E_tmax).apply(lambda x : x.magnitude)
    return df

def make_smoothed(daily_df):
    smoothed_group = daily_df.groupby(daily_df.index.dayofyear)
    smoothed_std = smoothed_group.std()
    print (smoothed_std)
    smoothed_val = smoothed_group.mean()
    smoothed_std.columns = ["std_"+ c for c in smoothed_std.columns]
    smoothed_df = pd.concat([smoothed_val,smoothed_std],axis=1)
    print (smoothed_df)
    return smoothed_df
    

for fname in csv_fnames:
    df = pd.read_csv(os.path.join("./CSV",fname),index_col="Date",converters={"Date":pd.to_datetime})
    daily_df = make_daily_avgs(df)
    fname_base = fname.split(".")[0]
    fname_to_write = fname_base + "_hourly.pkl"
    print (fname_to_write)

    fname_to_write_daily = fname_base + "_daily.pkl"
    fname_csv_daily = fname_base + "_daily.csv"
    fname_csv_averaged =  fname_base + "_AVG.csv"
    fname_pkl_averaged = fname_base+ "_AVG.pkl"
    smoothed_df = make_smoothed(daily_df)
    smoothed_df.to_pickle(fname_pkl_averaged)
    smoothed_df.to_csv(fname_csv_averaged)
    daily_df.to_csv(fname_csv_daily)
    df.to_pickle(fname_to_write)
    daily_df.to_pickle(fname_to_write_daily)
    
    

