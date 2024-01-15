
# A simple framework for Dataframe (Dask & Pandas dataframe) data processing tool (


## Usage
```py

# main.py
import DataframeHalfAutoPreprocess as dhap
import pandas as pd

df = pd.read_csv("sample.csv")
dhap.register.set_dataframe(df)
dhap.register.execurate()


# config.py
import DataframeHalfAutoPreprocess as dhap

@dhap.register.register
class col_A(dhap.DataProcessor):
    col_name = "A"
    d_type = "int"
    default_value = -1
    is_category = False

    def statisic(self):
        super().statisic()
        pass


```

