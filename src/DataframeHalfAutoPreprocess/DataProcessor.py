from typing import Any, Optional, List
from pandas import DataFrame
from multiprocessing import Pool
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

class DataProcessor:
    from_cols: List[Optional[str]] = []
    col_name: str = ""
    d_type: str = ""
    default_value: Optional[Any] = None
    is_category: bool = True

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self

    def process(self, df: DataFrame) -> None:

        if self.default_value is not None:
            # dask is not allow "inplace"
            df[self.col_name] = df[self.col_name].fillna(self.default_value)
        # if is_category:
        #     df[self.col_name] = df[self.col_name].astype(self.d_type)
        df[self.col_name] = df[self.col_name].astype(self.d_type)

    def transform(self, df: DataFrame, sample: DataFrame) -> None:
        if self.d_type == "str":
            le = LabelEncoder()
            le.fit(df[self.col_name])

    def preprocessing_with_sample(self, sample_df: DataFrame):
        if self.is_category or self.d_type == "str":
            pass

    def statistic(self, df: DataFrame):
        """
        mission value ratio
        distribution
        """
        # with Pool() as pool:
        # self.count_group
        # df.map_partitions(self.count_group)
        pass

    def run(self, df: DataFrame, sample_df: Optional[DataFrame] = None):
        self.process(df)
        self.statistic(df)
        self.transform(df, sample_df)


    def count_group(self, partition):
        pass
        # count_result = partition.groupby(self.col_name).count()
        # accumulated_counts.append(count_result)
        # print(count_result)

    def __init_subclass__(cls, **kwargs):
        """
        Ensure the subclas must contains non emptry string
        """
        for required in ('col_name', 'd_type'):
            if getattr(cls, required) == "":
                raise TypeError(f"Can't instantiate abstract class {cls.__name__} without {required} attribute defined")
        
        return super().__init_subclass__(**kwargs)

