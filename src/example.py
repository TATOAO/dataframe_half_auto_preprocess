
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
import dask.dataframe as dd
import json
from config import *

sample_csv = '../sample_1k.csv'
df = dd.read_csv(sample_csv, blocksize=1e2)

def count_group(partition):
    import ipdb;ipdb.set_trace()
    count_result = partition.groupby('E').count()
    # accumulated_counts.append(count_result)
    print(count_result)


# df.map_partitions(count_group)
dhap.register.set_dataframe(df)
dhap.register.set_pre_encoder_load_file('./pre_encoder.json')
dhap.register.execurate()


# dhap.register.set_dataframe(df, sample_size = 1e5)
# with open('...', 'r') as transformer_json:
#     dhap.register.load_transformer(json.load(transformer_json))

# print(dhap.register.get_column_names())
