import dask.dataframe as dd
from dask.diagnostics import ProgressBar

# Load your data into a Dask DataFrame
ddf = dd.read_csv('sample.csv', blocksize=1e2)

# Define your groupby operation without computing
result = ddf.groupby('A').count()

# Function to monitor the progress of your computation
async def monitor_progress(future, interval=5):
    with ProgressBar():
        while not future.done():
            # Here you might try to fetch intermediate results or just print the progress
            # Note: Fetching actual intermediate groupby results is non-trivial and might require a different approach
            print("Computing...")  # or any other indicator of progress
            await asyncio.sleep(interval)

# Use Dask's asynchronous API to compute the result
import asyncio
future = result.persist()  # starts computation in the background
asyncio.run(monitor_progress(future))

# When computation is done, you can retrieve the result
final_result = future.result()

