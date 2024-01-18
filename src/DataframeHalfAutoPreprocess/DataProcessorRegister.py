from typing import Dict, Optional, List
from pandas import DataFrame
from .DataProcessor import DataProcessor

class DataProcessorRegister:
    registed: Dict[str, DataProcessor] = {}
    registed_df:Optional[DataFrame] = None

    def set_dataframe(self, df: DataFrame):
        self.registed_df = df

    def __call__(self, cls: DataProcessor):
    # def register(self, cls):
        self.registed[cls.__name__] = cls()

    def get_column_names(self) -> List[str]:
        result: List[str] = []
        for col_processor in self.registed.values():
            result.append(col_processor.col_name)
        return result

    def execurate(self):
        for col_name, col_processor in self.registed.items():
            col_processor().run(self.registed_df)
        if self.registed_df is not None:
            result = self.registed_df.compute()
            return result




