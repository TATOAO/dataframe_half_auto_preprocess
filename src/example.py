
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
from config import *
sample_csv = '/home/atatlan/Work/dataframe_half_auto_preprocess/sample.csv'
df = pd.read_csv(sample_csv)
dhap.register.set_dataframe(df)
dhap.register.execurate()
