

from numpy import who
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
import dask.dataframe as dd
import json
from config import *

sample_csv = '../sample_1k.csv'
df = dd.read_csv(sample_csv, blocksize=1e2)

dhap.register.set_dataframe(df)
dhap.register.process()
