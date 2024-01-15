from utils import register
from config import *
import pandas as pd

if __name__ == "__main__":

    df = pd.read_csv('sample.csv')
    register.set_dataframe(df)
    register.execurate()

    print(df)




