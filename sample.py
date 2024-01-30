import pandas as pd
import numpy as np
import dask.dataframe as dd

N = int(100)
df = pd.DataFrame(np.random.randint(0,100,size=(N, 4)), columns=list('ABCD'))
df['E'] = np.random.choice(list('ABCD'), size = N)


dd_df = dd.from_pandas(df, npartitions=1)

print(df)

# print(dd_df.compute())

# dd_df.visualize()

