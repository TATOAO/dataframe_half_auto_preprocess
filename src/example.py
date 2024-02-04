
from numpy import who
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
import dask.dataframe as dd
import json
from config import *

sample_csv = '../sample_1k.csv'
df = dd.read_csv(sample_csv, blocksize=1e2)

# df.map_partitions(count_group)



####### example 1 fit and run ##
def example1():
    dhap.register.set_dataframe(df)
    dhap.register.set_pre_encoder_load_file('./pre_encoder.json')
    dhap.register.prepare_compute()
    dhap.register.process()


####### example 2 don't load directly run
def example2():
    dhap.register.set_dataframe(df)
    dhap.register.process()
    # should fail

####### example 3 load & run
def example3():
    dhap.register.set_dataframe(df)
    dhap.register.load_from_json('./pre_encoder.json')
    dhap.register.process()

def main():
    example1()
    
if __name__ == "__main__":
    main()

