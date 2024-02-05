import pandas as pd
import numpy as np
import dask.dataframe as dd

N = int(1000)
df = pd.DataFrame(np.random.randint(0,100,size=(N, 4)), columns=list('ABCD'))
df['E'] = np.random.choice(list('ABCD'), size = N)
df.loc[0:499, 'A'] = np.random.choice([1,2,3], size = 500)
df.loc[500:, 'A'] = np.random.choice([2,3,5], size = 500)

# dd_df = dd.from_pandas(df, npartitions=1)

print(df)

df.to_csv("sample_1k.csv")


# print(dd_df.compute())

# dd_df.visualize()

