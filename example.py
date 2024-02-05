from config import *
import DataframeHalfAutoPreprocess as dhap
import dask.dataframe as dd

if __name__ == "__main__":

    real_df = dd.read_csv('sample.csv', blocksize=1e6)
    dhap.register.set_pre_encoder_load_file('./src/pre_encoder_test.json')
    processed_df = dhap.register.process(real_df)
    import ipdb;ipdb.set_trace()




