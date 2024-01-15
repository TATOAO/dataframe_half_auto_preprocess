
# A simple framework for Dataframe (Dask & Pandas dataframe) data processing tool (


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


# main.py
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
from config import *

df = pd.read_csv("sample.csv")
dhap.register.set_dataframe(df)
dhap.register.execurate()




```

