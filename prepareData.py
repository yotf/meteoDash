import os
import pandas as pd
import numpy as np

csv_fnames = [d for d in os.listdir(".") if d.startswith("0000") and d.endswith(".csv")]

for fname in csv_fnames:
    df = pd.read_csv(fname,index_col="Date",converters={"Date":pd.to_datetime})
    fname_to_write = fname.split(".")[0] + ".pkl"
    print (fname_to_write)
    df.to_pickle(fname_to_write)
    

