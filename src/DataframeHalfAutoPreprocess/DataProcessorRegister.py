from typing import Dict, Optional, List, Union
from pandas import DataFrame
from .DataProcessor import DataProcessor
from .helper import MyEncoder, MinMaxScalerJson, OrdinalEncoderJson
from .json_helper import JsonSaverHelper
import json

class DataProcessorRegister:
    """
    Pipline:
        1. regist all column processor

        if [prepare]
        2. processing based on processor
            i) run i.e  preprocssing, statisics
                a) preprocessing includes:
                    1. fill null value
                    2. convert categorical values
            ii) generate a sample data 
            iii) fit a encoder
            iiii) save a json file that help predit with same config
        
        if [predict]
        2. processing based on processor
            i) load a json file
            ii) predict i.e  preprocssing
            
    """


    # saved class to process a column
    registed_processor_dict: Dict[str, DataProcessor] = {}
    registed_df:Optional[DataFrame] = None
    scalers_json: str = ""
    labelencoders_json: str = ""
    ## sample 
    sample_nrows: int = 100_000
    sample_ratio: float = 0.01
    sample_df:Optional[DataFrame] = None
    random_seed: int = 28938

    ## 
    transformer_dict: dict[str, Union[MinMaxScalerJson, OrdinalEncoderJson]] = {}
    file_name: str = './pre_encoder.json'
    json_helper: JsonSaverHelper = JsonSaverHelper(json_file_path = file_name)

    def get_all_categorical_columns_name(self) -> list[str]:
        return [processor.col_name 
                for processor in self.registed_processor_dict.values()]

    ################### main functions ############################## 

    def __call__(self, processor: type[DataProcessor]):
        """
        register the config class
        """
        self.registed_processor_dict[processor.__name__] = processor(
                json_helper = self.json_helper,
                file_name = self.file_name
                )

    def prepare_compute(self):
        """
        using the sample df of each column, doing some statistics and create a
        corresbonding transormfer 

        save it into pre_encoder.json
        """

        if self.sample_df is None:
            self.set_sample_dataframe()

        # process sample df and do statistic
        for col_name, col_processor in self.registed_processor_dict.items():
            if self.sample_df is None:
                raise ValueError("self.sample_df is None")
            col_processor.preprocess_with_statics(self.sample_df)

        # to fit category, the sample df must first be computed 
        self.sample_df = self.sample_df.compute()
        for col_name, col_processor in self.registed_processor_dict.items():
            col_processor.fit_transform(self.sample_df)

    def save_model(self):
        """
        must be run after "sample_compute"
        """
        for col_name, col_processor in self.registed_processor_dict.items():
            self.json_helper.add_model(col_name, col_processor.get_encoder())
            self.json_helper.write_to_json(self.file_name)

    def process(self, target_df: DataFrame):
        for _, col_processor in self.registed_processor_dict.items():
            if target_df is not None:
                categories_loaded = []
                if col_processor.judge_is_category():
                    encoder = col_processor.get_encoder()
                    if encoder is not None and isinstance(encoder, OrdinalEncoderJson):
                        categories_loaded = encoder.get_categories()

                col_processor.preprocess(target_df, categories_loaded)
                col_processor.prepare_run_transform(target_df)

        return target_df

    def sample_compute(self):
        if self.sample_df is None:
            raise ValueError("self.sample_df is None")

        return self.sample_df.compute()


    #########  util functions #############
    def set_dataframe(self, df: DataFrame) -> None:
        self.registed_df = df

    def set_sample_dataframe(self) -> None:
        """
        set the smaple dataframe
        """
        self.sample_df = self.get_sample_df()

    def set_sample_params(self, sample_nrows:Optional[int] = None, 
                                sample_ratio: Optional[int] = None) -> None:
        """
        Config the sample dataframe
        """

        if sample_nrows is not None:
            if self.registed_df is None:
                return None
            self.sample_nrows = sample_nrows
            self.sample_ratio = self.sample_nrows / len(self.registed_df)

        if sample_ratio is not None:
            self.sample_nrows = sample_ratio
            
    def set_pre_encoder_load_file(self, file_name:str = './pre_encoder.json') -> None:
        self.loaded_json_path = file_name
        self.json_helper.set_json_file_path(file_name)

    def get_sample_df(self, use_cache:bool = False) -> Optional[DataFrame]:
        if use_cache:
            return self.sample_df

        if self.registed_df is None:
            return None

        if self.sample_ratio is not None:
            sample_df = None
            while sample_df is None or len(sample_df) <= 10:
                sample_df = self.registed_df.sample(frac=self.sample_ratio, 
                                                    random_state=self.random_seed)
                if len(sample_df) <= 10:
                    self.sample_ratio += 0.01
            use_cache = True

            return sample_df


    def get_column_names(self) -> List[str]:
        result: List[str] = []
        for col_processor in self.registed_processor_dict.values():
            result.append(col_processor.col_name)
        return result





