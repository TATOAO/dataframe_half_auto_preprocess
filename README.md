
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
import json
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
dhap.register.set_pre_encoder_load_file('./pre_encoder.json') # default ./pre_encoder.json
dhap.register.set_statistic_save_file('./static.json') # defaultr 

# take the sample dataframe and output statistic and transformer
dhap.register.execurate() # generate statistic.json & transformer.json

# load the transformer, require "transfomer.json"
with open('...', 'r') as transformer_json:
    dhap.register.load_transformer(json.load(transformer_json))
    
    # use the transformer
    dhap.register.use()


# statistic & transformer () json 
{
    "col_A": {
        "col_name": "A",
        "transformer": {
            "label_encoder": {
                "encoder_id": "col_A_label_encoder"
            }
        },
        "statistic":{
            "counts": {
                [
                    {
                        "element": "大众", 
                        "counts": 20943,
                    },
                    {
                        "element": "宝马", 
                        "counts": 20943,
                    }
                ]
            }
        }
    },
    "col_B": {
        "col_name": "B",
        "transformer": {
            "min_max_scaler": {
                "encoder_id": "col_B_min_max_scaler"
            }
        },
        "statistic":{
            "percentails": [
                {
                    "persontail": 0.0,
                    "value": 2
                },
                {
                    "persontail": 0.25,
                    "value": 129
                },
                {
                    "persontail": 0.50,
                    "value": 129
                },
                {
                    "persontail": 0.75,
                    "value": 129
                },
                {
                    "persontail": 1.00,
                    "value": 12903
                }
            ],
            "mean": 193.232,
            "std": 23.232
        }
    }
}

# transformers (details)
{
    "col_A_label_encoder":{
        "classes": ["大众", "宝马", ... ]
    }
},
{
    "col_B_min_max_scaler":{
        "min": 2390.9,    
        "max": 39239.09,    
        "scaller": 2323
    }
}

```

## TODO

1. sample and visulualize statistic of columns
2. data preprocessing with sklearn processing
3. 

