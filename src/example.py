
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
import dask.dataframe as dd
from config import *

sample_csv = '../sample.csv'
df = dd.read_csv(sample_csv)
dhap.register.set_dataframe(df)
dhap.register.execurate()

print(dhap.get_column_names())
