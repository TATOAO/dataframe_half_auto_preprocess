
from numpy import who
import DataframeHalfAutoPreprocess as dhap
import pandas as pd
import dask.dataframe as dd
import json
from config import *

sample_csv = '../sample_1k.csv'
df = dd.read_csv(sample_csv, blocksize=1e2)


real_data = '../sample.csv'
real_df = dd.read_csv(real_data, blocksize=1e6)


####### example 1 fit and run ##
def example1():
    dhap.register.set_dataframe(df)
    dhap.register.set_pre_encoder_load_file('./pre_encoder.json')
    dhap.register.prepare_compute()
    dhap.register.save_model()
    processed_df = dhap.register.process(real_df)

####### example 2 don't load directly run
def example2():
    dhap.register.set_dataframe(df)
    dhap.register.process()
    # should fail

####### example 3 load & run
def example3():
    # dhap.register.load_from_json('./pre_encoder.json')
    dhap.register.set_pre_encoder_load_file('./pre_encoder_test.json')
    processed_df = dhap.register.process(real_df)
    print(processed_df.head())

def main():
    example1()

if __name__ == "__main__":
    main()
