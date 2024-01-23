from dask.distributed import Client, as_completed
import dask.dataframe as dd
import asyncio

# Set up Dask distributed client
def main():
    client = Client()

    # Load your data into a Dask DataFrame
    ddf = dd.read_csv('sample.csv', blocksize=10e6)

    # Define your groupby operation without computing
    result = ddf.groupby('A').count()

    # Persist starts computation in the background and returns a Dask Future
    import ipdb;ipdb.set_trace()
    future = client.persist(result)


    final_result = future.result()

if __name__ == "__main__":
    main()


# Function to monitor the progress of your computation
# async def monitor_progress(future):
#     futures = [future]
#     for f in as_completed(futures):
#         result = await f  # This line gets the result of computation
#         print("One of the computations is complete.")
#         # Process the result here or just print a statement
#
# async def main():
#     # Use Dask's asynchronous API to compute the result
#     await monitor_progress(future)
#
# # Run the main function
# asyncio.run(main())
#
# When computation is done, you can retrieve the result

