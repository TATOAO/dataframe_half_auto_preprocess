
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
import dask.dataframe as dd
from config import *
sample_csv = '/home/atatlan/Work/dataframe_half_auto_preprocess/sample.csv'
df = dd.read_csv(sample_csv)
dhap.register.set_dataframe(df)
dhap.register.execurate()
import ipdb;ipdb.set_trace()
