# coding: utf-8
fnames = [f for f in os.listdir(".") if f.endswith(".w6d")]
import os
fnames = [f for f in os.listdir(".") if f.endswith(".w6d")]
fnames
for f in fnames:
    pd.read_csv(f,,sep="\s+",index_col="DATE")
pd.to_datetime(arg=z.index,format="%Y%j")
import pandas as pd
for f in fnames:
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=z.index,format="%Y%j")
    
for f in fnames:
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    
    
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    
    
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    
    
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()

    
    
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=stderr.TMAX)
    

    
    
import matplotlib.pyplot as plt
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=stderr.TMAX)
    

    
    
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    
    

    
    
plt.show()
import seaborn as sns
sns.set()
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.figure()
    
    
    

    
    
plt.show()
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.figure()
    
    
    

    
    
plt.show()
for f in fnames:
    print(f)
    plt.figure()
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    
    
    
    

    
    
plt.show()
for f in fnames:
    print(f)
    plt.figure()
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.xaxis("TMAX")
    plt.yaxis("Day Of Year")
    
    
    
    
    

    
    
for f in fnames:
    print(f)
    plt.figure()
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.xlabel("TMAX")
    plt.ylabel("Day Of Year")
    
    
    
    
    
    

    
    
plt.show()
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.ylabel("TMAX")
    plt.xlabel("Day Of Year")
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMIN,yerr=std.TMIN)
    plt.ylabel("TMIN")
    plt.xlabel("Day Of Year")
    
    
    
    
    
    
    

    
    
plt.show()
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.ylabel("TMAX")
    plt.xlabel("Day Of Year")
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMIN,yerr=std.TMIN)
    plt.title(f)
    plt.ylabel("TMIN")
    plt.xlabel("Day Of Year")
    
    
    
    
    
    
    
    

    
    
plt.show()
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.ylabel("TMAX")
    plt.xlabel("Day Of Year")
    plt.savefig(f.split(".")[0]+"TMAX",format="svg")
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMIN,yerr=std.TMIN)
    plt.title(f)
    plt.ylabel("TMIN")
    plt.xlabel("Day Of Year")
    plt.savefig(f.split(".")[0]+"TMIN",format="svg")
    
    
    
    
    
    
    
    
    

    
    
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.ylabel("TMAX")
    plt.xlabel("Day Of Year")
    plt.savefig(f.split(".")[0]+"_TMAX.svg",format="svg")
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMIN,yerr=std.TMIN)
    plt.title(f)
    plt.ylabel("TMIN")
    plt.xlabel("Day Of Year")
    plt.savefig(f.split(".")[0]+"_TMIN.svg",format="svg")
    
    
    
    
    
    
    
    
    
    

    
    
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.ylabel("TMAX")
    plt.xlabel("Day Of Year")
    plt.savefig(f.split(".")[0]+"_TMAX.svg",format="png",dpi=300)
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMIN,yerr=std.TMIN)
    plt.title(f)
    plt.ylabel("TMIN")
    plt.xlabel("Day Of Year")
    plt.savefig(f.split(".")[0]+"_TMIN.svg",format="png",dpi=300)
    
    
    
    
    
    
    
    
    
    
    

    
    
for f in fnames:
    print(f)
    df=pd.read_csv(f,sep="\s+",index_col="DATE")
    df.index = pd.to_datetime(arg=df.index,format="%Y%j")
    print (df)
    grouped = df.groupby(df.index.dayofyear)
    std = grouped.std()
    mean = grouped.mean()
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMAX,yerr=std.TMAX)
    plt.title(f)
    plt.ylabel("TMAX")
    plt.xlabel("Day Of Year")
    plt.savefig(f.split(".")[0]+"_TMAX.png",format="png",dpi=300)
    plt.figure()
    plt.errorbar(x=mean.index,y=mean.TMIN,yerr=std.TMIN)
    plt.title(f)
    plt.ylabel("TMIN")
    plt.xlabel("Day Of Year")
    plt.savefig(f.split(".")[0]+"_TMIN.png",format="png",dpi=300)
    
    
    
    
    
    
    
    
    
    
    

    
    
get_ipython().run_line_magic('save', 'current_session ~0/')
