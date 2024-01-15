import pandas as pd
import numpy as np
import dask.dataframe as dd

N = 100
df = pd.DataFrame(np.random.randint(0,100,size=(N, 4)), columns=list('ABCD'))
df['E'] = np.random.choice(list('ABCD'), size = N)

df.to_csv("sample.csv")

# dd_df = dd.from_pandas(df, npartitions=1)


# print(dd_df.compute())

# dd_df.visualize()

