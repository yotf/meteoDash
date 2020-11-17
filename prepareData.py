import os
import pandas as pd
import numpy as np
from metpy.calc import thermo
from metpy.units import units
from lcl_berkley import lcl as lclb


klim_folder = "./source_CSV/Klimatologija/1971_2000"
PIS_folder = "./source_CSV/PIS"
output_klim = "./CSV/Klimatologija"
other_folder = "./source_CSV/other/"
csv_fnames = [d for d in os.listdir(PIS_folder) if d.startswith("0000") and d.endswith(".csv")]
klim_fnames = [f for f in os.listdir(klim_folder) if f.endswith(".w6d")]
other_fnames = [f for f in os.listdir(other_folder) ]
output_klim = "./source_CSV/Klimatologija/1971_2000/CALC"

def format_hourly(hourly_df):
    hourly_df = hourly_df[['HC Air temperature [°C] avg','HC Relative humidity [%] avg',
                           'Precipitation [mm] sum','Soil temperature [°C] avg']]
    hourly_df.columns=["Tavg","RH","Precipitation","SAvg"]
    return hourly_df



    
    
def calculate_hourly(hourly_df):
    """Calculates values for hourly data.Takes raw csv period data, 
changes names and calculates LCL and qsat and q and dewpoint"""
    kelvin_difference = 273.15
    pressure = 101325.0 *units.pascal
    
    hourly_df.RH = hourly_df.RH/100
    hourly_df = hourly_df[hourly_df.RH!=0] #izbacujemo sve kolone koje imaju u RH nulu
    hourly_df["dewpoint"] = hourly_df.apply(lambda x : thermo.dewpoint_rh(x.Tavg* units.celsius,x.RH),axis=1).apply(lambda x: x.magnitude)
    hourly_df["q"] = hourly_df.apply(lambda x: thermo.mixing_ratio_from_relative_humidity(x.RH,x.Tavg*units.celsius, pressure),axis=1).apply(lambda x: thermo.specific_humidity_from_mixing_ratio(x)).apply(lambda x: x.magnitude)
    hourly_df["qsat"] = hourly_df.apply(lambda x : thermo.saturation_mixing_ratio(pressure,x.Tavg * units.celsius),axis=1).apply(lambda x: thermo.specific_humidity_from_mixing_ratio(x)).apply(lambda x: x.magnitude)
    hourly_df["lcl"] = hourly_df.apply(lambda x: lclb.lcl(pressure.magnitude,x.Tavg + kelvin_difference,x.RH),axis=1)
    return hourly_df
def convert_to_daily(hourly_df):
    """converts to daily"""
    mindf = hourly_df.Tavg.resample('D').min()
    maxdf = hourly_df.Tavg.resample('D').max()
    padavine_daily = hourly_df.Precipitation.resample('D').sum()
    hourly_df.drop(columns=["Precipitation"],inplace=True)
    zz = pd.concat([mindf,maxdf],axis=1)
    zz.columns = ["Tmin","Tmax"]
    df = pd.concat([hourly_df.resample('D').mean(),zz,padavine_daily],axis=1)
    return df

def make_daily_avgs(df):
    """ Takes daily data, calculates"""

    Lv = 2265.705 *1000 #grami
    Cp = 1003 # J/kg
    pressure = 101325.0 *units.pascal
    df["tendt"] = Cp*df.Tavg.diff()/(24*3600)
    df["tendq"] = (Lv*df.q.diff()/(24*3600)) 
    df["bowen"] = (Cp*df.Tavg.diff())/(Lv*df.q.diff())
    df["qsat"] =df.apply(
        lambda x : thermo.saturation_mixing_ratio(pressure,x.Tmin * units.celsius),axis=1).apply(
        lambda x: thermo.specific_humidity_from_mixing_ratio(x)).apply(
            lambda x: x.magnitude
        )
    df.loc[(df.bowen>20) | (df.bowen<-20),"bowen"]=None
    E_tmin = df.Tmin.apply(lambda x: thermo.saturation_vapor_pressure(x * units.celsius))
    E_tmax = df.Tmax.apply(lambda x: thermo.saturation_vapor_pressure(x* units.celsius))
    E_avg = df.Tavg.apply(lambda x: thermo.saturation_vapor_pressure(x* units.celsius))
    df["R2"] = (E_tmin/E_tmax).apply(lambda x: x.magnitude)
    df["R1"] =  ((df.RH*E_avg)/E_tmax).apply(lambda x : x.magnitude)
    return df

def make_smoothed(daily_df):
    """Pravi visegodisnje srednjake od dnevnih vrednosti"""
    smoothed_group = daily_df.groupby(daily_df.index.dayofyear)
    print(daily_df.index[0],daily_df.index[-1])
    smoothed_val = smoothed_group.mean()
    smoothed_std = smoothed_group.std()
    smoothed_std.columns = ["std_"+ c for c in smoothed_std.columns]
    smoothed_df = pd.concat([smoothed_val,smoothed_std],axis=1)
    smoothed_df["period_start"] = [str(daily_df.index[0])]*len(smoothed_df.index)
    smoothed_df["period_end"] = [str(daily_df.index[-1])]*len(smoothed_df.index)
    za_rolling = [c for c in smoothed_df.columns if (not c.startswith("Date") and not c.startswith("std") and not c.startswith("period"))]
    print (za_rolling)
    for col in za_rolling:
        smoothed_df["rolling_mean"+col] = smoothed_df[col].rolling(10).mean()
        smoothed_df["rolling_std_"+col] = smoothed_df[col].rolling(10).std()
    print (smoothed_df)
    return smoothed_df



for fname in csv_fnames:
    def make_fname(fname_base,pstart,pend,suffix):
        return "_".join(fname_base.split("_")[0:4]+ [str(pstart.date()),str(pend.date()),suffix])
    df_hourly = pd.read_csv(os.path.join(PIS_folder,fname),index_col="Date",converters={"Date":pd.to_datetime})
    df_hourly = format_hourly(df_hourly)
    df_hourly = calculate_hourly(df_hourly)
    daily_df = convert_to_daily(df_hourly)
    daily_df = make_daily_avgs(daily_df)
    pstart,pend = daily_df.index[0],daily_df.index[-1]
    fname_base = fname.split(".")[0]
    fname_to_write = make_fname(fname_base,pstart,pend,"hourly.pkl")
    fname_hourly_csv = make_fname(fname_base,pstart,pend,"hourly.csv")
    print (fname_to_write)
    fname_to_write_daily = make_fname(fname_base,pstart,pend, "daily.pkl")
    fname_csv_daily = make_fname(fname_base,pstart,pend, "daily.csv")
    fname_csv_averaged = make_fname(fname_base,pstart,pend, "AVG.csv")
    smoothed_df = make_smoothed(daily_df)
    fname_pkl_averaged = make_fname(fname_base,pstart,pend,"AVG.pkl")
    print (fname_pkl_averaged)
    smoothed_df.to_pickle(fname_pkl_averaged)
    smoothed_df.to_csv(fname_csv_averaged)
    daily_df.to_csv(fname_csv_daily)
    df_hourly.to_pickle(fname_to_write)
    df_hourly.to_csv(fname_hourly_csv)
    daily_df.to_pickle(fname_to_write_daily)
def format_other(df):
    df = df.rename(columns={'HC Air temperature [°C] avg':"Tavg",'HC Air temperature [°C] min':"Tmin",'HC Air temperature [°C] max':"Tmax",'HC Relative humidity [%] avg':"RH",
                           'Precipitation [mm] sum':"Precipitation"})
    print (df)
    return df

for fname in other_fnames:
    df = pd.read_csv(os.path.join(other_folder,fname),index_col="Date",converters={"Date":lambda x:pd.to_datetime(x,format="%d/%m/%Y")})
    df = format_other(df)
    df = calculate_hourly(df)
    df_daily = make_daily_avgs(df)
    smoothed_df= make_smoothed(df_daily)
    df_daily.to_pickle("00000CWA_CWA_CWA_CWA_1998_2019_daily.pkl")
    df_daily.to_csv("00000CWA_CWA_CWA_CWA_1998_2019_daily.csv")
    smoothed_df.to_pickle("00000CWA_CWA_CWA_CWA_1998_2019_AVG.pkl")
    smoothed_df.to_csv("00000CWA_CWA_CWA_CWA_1998_2019_AVG.csv")

    



for fname in klim_fnames:
    import numpy as np
    Lv = 2265.705 *1000 #grami
    Cp = 1003 # J/kg
    base = fname.split("_")[0] 
    z = pd.read_csv(os.path.join(klim_folder,fname),delim_whitespace=True,index_col="DATE")
    kelvin_offset = 273.15
    pressure = 101325.0 *units.pascal
    z= z[(z.TMIN<66) & (z.TMIN> -66)]
    print (z.loc[~(np.abs(z.VAPO-z.VAPO.mean()) <= (3*z.VAPO.std())),'VAPO'])
#    z.loc[~(np.abs(z.VAPO-z.VAPO.mean()) <= (3*z.VAPO.std())),'VAPO'] = np.nan
    print ("NONE's")
    print (z.isnull().any())
    z.VAPO.interpolate(inplace=True)
    print ("NONE's")
    print (z.isnull().any())
    z["q"] = 0.622* (z.VAPO/pressure)
    z.q = z.q*100
    z.rename(columns = {"TMIN":"Tmin","TMAX":"Tmax","DATE":"Date"},inplace=True)
    z["Tavg"] = (z.Tmax+z.Tmin)/2
    z["qsat"] = z.apply(lambda x: thermo.specific_humidity_from_mixing_ratio(thermo.saturation_mixing_ratio(tot_press = pressure,temperature = x.Tavg * units.celsius)).magnitude,axis=1)
    z["RH2"] = z.apply(lambda x :thermo.relative_humidity_from_specific_humidity(specific_humidity=x.q,temperature = x.Tavg* units.celsius,pressure = pressure),axis=1).apply(lambda x: x.magnitude)
    z["RH"] = z.apply(lambda x :x.VAPO/thermo.saturation_vapor_pressure(x.Tavg* units.celsius).magnitude,axis=1)
    print (fname)
    z["dewpoint"] = z.apply(lambda x : thermo.dewpoint_rh(x.Tavg* units.celsius,x.RH),axis=1).apply(lambda x: x.magnitude)
    z["lcl"] = z.apply(lambda x: lclb.lcl(T=x.Tavg +kelvin_offset,p=pressure.magnitude,rh = x.RH),axis=1)
    z["tendt"] = Cp*z.Tavg.diff()/(24*3600)
    z["tendq"] = Lv*z.q.diff()/(24*3600)
    z["bowen"] = (Cp*z.Tavg.diff())/(Lv*z.q.diff())
    z.loc[(z.bowen>5) | (z.bowen<-5),"bowen"] = None
#    z.bowen[(z.bowen>5) | (z.bowen<0)] = None
    E_tmin = z.Tmin.apply(lambda x: thermo.saturation_vapor_pressure(x * units.celsius))
    E_tmax = z.Tmax.apply(lambda x: thermo.saturation_vapor_pressure(x* units.celsius))
    E_avg = z.Tavg.apply(lambda x: thermo.saturation_vapor_pressure(x* units.celsius))
    z["R2"] = (E_tmin/E_tmax).apply(lambda x: x.magnitude)
    z["R1"] =  ((z.RH*E_avg)/E_tmax).apply(lambda x : x.magnitude)
    z.index = pd.to_datetime(arg=z.index,format="%Y%j")
    z.to_pickle("00000%s_%s_%s_%s_%s_%s_daily.pkl" %(base,base,base,base,"1971","2000"))
    z.to_csv("%s_O_daily.csv" %base)
    grouped = z.groupby(z.index.dayofyear)
    std = grouped.std()
    std.columns = ["std_"+c for c in std.columns]
    mean = grouped.mean()
    gdf = pd.concat([std,mean],axis=1)
    for col in [c for c in mean.columns if not "DATE" in c]:
       rol = mean[col].rolling(10)
       gdf["rolling_mean_" + col] = rol.mean()
       gdf["rolling_std_" + col] = rol.std()
    gdf.to_pickle("00000%s_%s_%s_%s_%s_%s_AVG.pkl" %(base,base,base,base,"1971","2000"))
    gdf.to_csv("%s_O_AVG.csv" %base)

    
    
    
    

