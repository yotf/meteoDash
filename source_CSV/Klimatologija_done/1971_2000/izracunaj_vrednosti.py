import pandas as pd
import os
from metpy.units import units
from metpy.calc import thermo
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
pressure = 101325.0 *units.pascal
fnames = [f for f in os.listdir(".") if f.endswith(".w6d")]
kelvin_offset = 273.15
def lcl(p,T,rh=None,rhl=None,rhs=None,return_ldl=False,return_min_lcl_ldl=False):

   import math
   import scipy.special

   # Parameters
   Ttrip = 273.16     # K
   ptrip = 611.65     # Pa
   E0v   = 2.3740e6   # J/kg
   E0s   = 0.3337e6   # J/kg
   ggr   = 9.81       # m/s^2
   rgasa = 287.04     # J/kg/K 
   rgasv = 461        # J/kg/K 
   cva   = 719        # J/kg/K
   cvv   = 1418       # J/kg/K 
   cvl   = 4119       # J/kg/K 
   cvs   = 1861       # J/kg/K 
   cpa   = cva + rgasa
   cpv   = cvv + rgasv

   # The saturation vapor pressure over liquid water
   def pvstarl(T):
      return ptrip * (T/Ttrip)**((cpv-cvl)/rgasv) * \
         math.exp( (E0v - (cvv-cvl)*Ttrip) / rgasv * (1/Ttrip - 1/T) )
   
   # The saturation vapor pressure over solid ice
   def pvstars(T):
      return ptrip * (T/Ttrip)**((cpv-cvs)/rgasv) * \
         math.exp( (E0v + E0s - (cvv-cvs)*Ttrip) / rgasv * (1/Ttrip - 1/T) )

   # Calculate pv from rh, rhl, or rhs
   rh_counter = 0
   if rh  is not None:
      rh_counter = rh_counter + 1
   if rhl is not None:
      rh_counter = rh_counter + 1
   if rhs is not None:
      rh_counter = rh_counter + 1
   if rh_counter != 1:
      print(rh_counter)
      exit('Error in lcl: Exactly one of rh, rhl, and rhs must be specified')
   if rh is not None:
      # The variable rh is assumed to be 
      # with respect to liquid if T > Ttrip and 
      # with respect to solid if T < Ttrip
      if T > Ttrip:
         pv = rh * pvstarl(T)
      else:
         pv = rh * pvstars(T)
      rhl = pv / pvstarl(T)
      rhs = pv / pvstars(T)
   elif rhl is not None:
      pv = rhl * pvstarl(T)
      rhs = pv / pvstars(T)
      if T > Ttrip:
         rh = rhl
      else:
         rh = rhs
   elif rhs is not None:
      pv = rhs * pvstars(T)
      rhl = pv / pvstarl(T)
      if T > Ttrip:
         rh = rhl
      else:
         rh = rhs
   if pv > p:
      return None

   # Calculate lcl_liquid and lcl_solid
   qv = rgasa*pv / (rgasv*p + (rgasa-rgasv)*pv)
   rgasm = (1-qv)*rgasa + qv*rgasv
   cpm = (1-qv)*cpa + qv*cpv
   if rh == 0:
      return cpm*T/ggr
   aL = -(cpv-cvl)/rgasv + cpm/rgasm
   bL = -(E0v-(cvv-cvl)*Ttrip)/(rgasv*T)
   cL = pv/pvstarl(T)*math.exp(-(E0v-(cvv-cvl)*Ttrip)/(rgasv*T))
   aS = -(cpv-cvs)/rgasv + cpm/rgasm
   bS = -(E0v+E0s-(cvv-cvs)*Ttrip)/(rgasv*T)
   cS = pv/pvstars(T)*math.exp(-(E0v+E0s-(cvv-cvs)*Ttrip)/(rgasv*T))
   lcl = cpm*T/ggr*( 1 - \
      bL/(aL*scipy.special.lambertw(bL/aL*cL**(1/aL),-1).real) )
   ldl = cpm*T/ggr*( 1 - \
      bS/(aS*scipy.special.lambertw(bS/aS*cS**(1/aS),-1).real) )

   # Return either lcl or ldl
   if return_ldl and return_min_lcl_ldl:
      exit('return_ldl and return_min_lcl_ldl cannot both be true')
   elif return_ldl:
      return ldl
   elif return_min_lcl_ldl:
      return min(lcl,ldl)
   else:
      return lcl
  
Lv = 2265.705
Cp = 1.003
  
for f in fnames:
    print(f)
    z=pd.read_csv(f,delim_whitespace=True,index_col="DATE")
    z= z[(z.TMIN<66) & (z.TMIN> -66)]
    z["q"] = 0.622* (z.VAPO/pressure)
    z.q = z.q*100
    z["TAVG"] = (z.TMAX+z.TMIN)/2
    z["RH"] = z.apply(lambda x :thermo.relative_humidity_from_specific_humidity(specific_humidity=x.q,temperature = x.TAVG* units.celsius,pressure = pressure),axis=1).apply(lambda x: x.magnitude)
    print (z.RH[z.RH>1])
    print (f)
    z["dewpoint"] = z.apply(lambda x : thermo.dewpoint_rh(x.TAVG* units.celsius,x.RH),axis=1).apply(lambda x: x.magnitude)
    z["lcl"] = z.apply(lambda x: lcl(T=x.TAVG +kelvin_offset,p=pressure.magnitude,rh = x.RH),axis=1)
    z["tendt"] = Cp*z.TAVG.diff()/(24*3600)
    z["tendq"] = Lv*z.q.diff()/(24*3600)
    z["bowen"] = (Cp*z.TAVG.diff())/(Lv*z.q.diff())
    z.bowen[(z.bowen>5) | (z.bowen<-5)] = None
#    z.bowen[(z.bowen>5) | (z.bowen<0)] = None
    E_tmin = z.TMIN.apply(lambda x: thermo.saturation_vapor_pressure(x * units.celsius))
    E_tmax = z.TMAX.apply(lambda x: thermo.saturation_vapor_pressure(x* units.celsius))
    E_avg = z.TAVG.apply(lambda x: thermo.saturation_vapor_pressure(x* units.celsius))
    z["R2"] = (E_tmin/E_tmax).apply(lambda x: x.magnitude)
    z["R1"] =  ((z.RH*E_avg)/E_tmax).apply(lambda x : x.magnitude)
    z.to_csv("CALC_"+f.split(".")[0]+".csv")
    z.index = pd.to_datetime(arg=z.index,format="%Y%j")
    grouped = z.groupby(z.index.dayofyear)
    std = grouped.std()
    std.columns = ["std_"+c for c in std.columns]
    mean = grouped.mean()
    gdf = pd.concat([std,mean],axis=1)
 
    print (gdf)
    for col in [c for c in mean.columns if not "DATE" in c]:
       rol = mean[col].rolling(10)
       gdf["rolling_mean_" + col] = rol.mean()
       gdf["rolling_std_" + col] = rol.std()
    print (gdf)
    gdf.to_csv("srednjak_"+f.split(".")[0]+".csv")
      
            
#        plt.figure()
#        plt.errorbar(x=mean.index,y=mean[col],yerr=std[col])
#        plt.title(f)
#        plt.ylabel(col)
#        plt.xlabel("Day Of Year")

#    plt.show()


    
