
# A simple framework for Dataframe (Dask & Pandas dataframe) data processing tool 


## input 

1. raw data
2. column process methods

## ouput
1. label encoder
2. scaler 
3. processed data


## Usage
```py
# config.py
import DataframeHalfAutoPreprocess as dhap

@dhap.register
class col_A(dhap.DataProcessor):
    col_name = "A"
    d_type = "int"
    default_value = -1
    is_category = False
    sample_nrow = 100


# main.py
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
from config import *

df = pd.read_csv("sample.csv")
dhap.register.set_dataframe(df)
dhap.register.execurate()


```

## TODO

1. sample and visulualize statistic of columns
2. data preprocessing with sklearn processing
3. 

