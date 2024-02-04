from typing import Any, Optional, List, Union
from pandas import DataFrame
import pandas as pd
from .helper import OrdinalEncoderJson, MinMaxScalerJson, MyEncoder
from .json_helper import JsonSaverHelper


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
    json_helper: JsonSaverHelper
    file_name: str

    def __init__(self, json_helper: JsonSaverHelper, file_name: str):
        self.json_helper = json_helper
        self.file_name = file_name

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self

    def __init_subclass__(cls, **kwargs):
        """
        Ensure the subclas must contains non emptry string
        """
        for required in ('col_name', 'd_type'):
            if getattr(cls, required) == "":
                raise TypeError(f"Can't instantiate abstract class {cls.__name__} without {required} attribute defined")
                col_processor.get_encoder()
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
        df[self.col_name] = df[self.col_name].astype(self.d_type)

        if self.judge_is_category():
            if self.encoder is not None:
                pass
            self.categorical_preprocess(df, categories)

    def prepare_run_transform(self, df: DataFrame) -> None:
        """
        Lacily run encoder transfrom process
        """
        encoder = self.get_encoder()
        df[self.col_name] = encoder.transform(df[[self.col_name]])[self.col_name]

    def fit_transform(self, sample_df: DataFrame) -> \
                Union[OrdinalEncoderJson, MinMaxScalerJson]:
        """
        Fit the encoder actively
        return the fitted encoder
        """

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
        calculate the statistic including and output:
        1. mission value ratio
        2. distribution
        """
        if self.judge_is_category():
            counting_result = sample_df.groupby(self.col_name).count().compute()
            print(counting_result)

    def preprocess_with_statics(self, sample_df:DataFrame) -> None:
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

    def get_encoder(self) -> Union[OrdinalEncoderJson, MinMaxScalerJson, None]:
        if self.encoder is not None:
            return self.encoder
        else:
            # try to load from json file
            if self.file_name is None:
                # raise Exception("Get Encoder Fail, neither encoder setup nor json file")
                return None
            return self.json_helper.get_encoder(self.col_name)
        

    ##################### below is for categotical computation ##################


    def categorical_load_process(self, df):
        encoder: OrdinalEncoderJson = self.get_encoder()
        categories = encoder.get_categories()
        df[self.col_name] = df[self.col_name].astype(
                pd.api.types.CategoricalDtype(categories, ordered=True))

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
        # df = df.categorize(columns = [self.col_name])

    def judge_is_category(self):
        """
        judge whether this column is categorical
        """
        return self.is_category or self.d_type == "str" or self.d_type == 'object'

    ##################### below is for statisics ##################


