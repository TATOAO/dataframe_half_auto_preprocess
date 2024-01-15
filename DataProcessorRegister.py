from typing import Dict, Optional
from pandas import DataFrame
from DataProcessor import DataProcessor

class DataProcessorRegister:
    registed = {}
    registed_df:Optional[DataFrame] = None

    def set_dataframe(self, df: DataFrame):
        self.registed_df = df

    def register(self, cls):
        self.registed[cls.__name__] = cls()

    def execurate(self):
        for col_name, col_processor in self.registed.items():
            col_processor().run(self.registed_df)
        pass




