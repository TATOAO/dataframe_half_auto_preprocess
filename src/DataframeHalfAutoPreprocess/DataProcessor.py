from typing import Any, Optional, List, Union
from pandas import DataFrame
import pandas as pd
from multiprocessing import Pool
import json
from .helper import OrdinalEncoderJson, MinMaxScalerJson, MyEncoder


class DataProcessor:
    """
    All calculation should be lazy, this module is designed for Dask Dataframe

    in preparing
    input:
        1. col_name
        2. dataframe

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
    encoder: Any = None

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

    ##################### main methods below #################################
    def preprocess(self, df: DataFrame, categories: list[str] = []) -> None:
        """
        1. fill na data
        2. convert data type
        """
        if self.default_value is not None:
            # dask is not allow "inplace"
            df[self.col_name] = df[self.col_name].fillna(self.default_value)
        # df[self.col_name] = df[self.col_name].astype(self.d_type)

        if self.judge_is_category():
            self.categorical_preprocess(df, categories)


    def fit_transform(self, sample_df: DataFrame) -> \
                Union[OrdinalEncoderJson, MinMaxScalerJson]:

        if self.judge_is_category():
            lbe = OrdinalEncoderJson(encoder_id = self.col_name)
            lbe.fit(sample_df[[self.col_name]])
            self.encoder = lbe
        else:
            min_max_scaler = MinMaxScalerJson(encoder_id = self.col_name)
            min_max_scaler.fit(sample_df[[self.col_name]])
            self.encoder = min_max_scaler
        return self.encoder


    def statistic(self, sample_df: DataFrame):
        """
        mission value ratio
        distribution
        need to be sub 
        """
        if self.judge_is_category():

            counting_result = sample_df.groupby(self.col_name).count().compute()
            print(counting_result)


    def after_run(self, df, categories):
        """
        no 
        """
        self.preprocess(df, categories)

    def run(self, df:DataFrame) -> None:
        self.preprocess(df)

    def run_with_statics(self, sample_df:DataFrame) -> None:
        """
        all runing should be lazy
        1. do the statistic
        2. save into categories

        self.preprocess(df)
        self.statistic(sample_df)
        self.fit_transform(sample_df)
        """

        self.preprocess(sample_df)
        self.statistic(sample_df)

    def get_encoder(self) -> Union[OrdinalEncoderJson, MinMaxScalerJson]:
        return self.encoder

    ##################### below is for categotical computation ##################

    def categorical_preprocess(self, df: DataFrame, categories: list[str]) -> None:
        """
        should run lazily
        """
        if len(categories) == 0:
            df[self.col_name] = df[self.col_name].astype('category')
        else:
            df[self.col_name] = df[self.col_name].astype(
                    pd.api.types.CategoricalDtype(categories, ordered=True)
                )
        df = df.categorize(columns = [self.col_name])

    def get_categories(self, df) -> list[str]:
        return df[self.col_name].categories

    def judge_is_category(self):
        """
        judge whether this column is categorical
        """
        return self.is_category or self.d_type == "str" or self.d_type == 'object'



    ##################### below is for statisics ##################


