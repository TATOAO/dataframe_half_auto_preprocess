from typing import Any, Optional, List, Union
from pandas import DataFrame
from multiprocessing import Pool
import json
from .helper import OrdinalEncoderJson, MinMaxScalerJson, MyEncoder


class DataProcessor:
    """
    in preparing

    1. fill na
    2. convert data
        i.e. turn to categorical data,

    in predicting

    1. fill na
    2. accept config from json file


    """
    from_cols: List[Optional[str]] = []
    col_name: str = ""
    d_type: str = ""
    default_value: Optional[Any] = None
    is_category: bool = True

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self

    def __init_subclass__(cls, **kwargs):
        """
        Ensure the subclas must contains non emptry string
        """
        for required in ('col_name', 'd_type'):
            if getattr(cls, required) == "":
                raise TypeError(f"Can't instantiate abstract class {cls.__name__} without {required} attribute defined")
        
        return super().__init_subclass__(**kwargs)

    def preprocess(self, df: DataFrame) -> None:
        """
        1. fill na data
        2. convert data type
        """
        if self.default_value is not None:
            # dask is not allow "inplace"
            df[self.col_name] = df[self.col_name].fillna(self.default_value)
        df[self.col_name] = df[self.col_name].astype(self.d_type)
            

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

    def run(self, df: Optional[DataFrame], 
            sample_df: Optional[DataFrame] = None,
            to_save_list: List = []):
        """
        self.preprocess(df)
        self.statistic(sample_df)
        self.fit_transform(sample_df)
        """

        self.preprocess(df)
        self.statistic(df)
        to_save_list.append(self.fit_transform(sample_df))

    def fit_transform(self, sample_df):

        if self.is_category or self.d_type == "str" or self.d_type == 'object':
            lbe = OrdinalEncoderJson(encoder_id = self.col_name)
            lbe.fit(sample_df[[self.col_name]])
            return lbe
        else:
            min_max_scaler = MinMaxScalerJson(encoder_id = self.col_name)
            min_max_scaler.fit(sample_df[[self.col_name]])
            return min_max_scaler

    ##################### below is for statisics ##################

    def count_group(self, partition):
        pass
        # count_result = partition.groupby(self.col_name).count()
        # accumulated_counts.append(count_result)
        # print(count_result)

