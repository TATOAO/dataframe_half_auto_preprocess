from typing import Dict, Optional, List
from pandas import DataFrame
from .DataProcessor import DataProcessor
from .helper import MyEncoder
import json

class DataProcessorRegister:
    registed: Dict[str, DataProcessor] = {}
    registed_df:Optional[DataFrame] = None
    scalers_json: str = ""
    labelencoders_json: str = ""
    sample_nrows: int = 100_000
    sample_ratio: float = 0.01
    sample_df:Optional[DataFrame] = None
    random_seed: int = 28938
    file_name: str = './pre_encoder.json'
    transformer_dict: dict = {}

    def __init__(self):
        pass

    def set_dataframe(self, df: DataFrame) -> None:
        self.registed_df = df

    def set_sample_dataframe(self) -> None:
        self.sample_df = self.get_sample_df()

    def set_sample_params(self, sample_nrows:Optional[int] = None, 
                                sample_ratio: Optional[int] = None) -> None:

        if sample_nrows is not None:
            if self.registed_df is None:
                return None
            self.sample_nrows = sample_nrows
            self.sample_ratio = self.sample_nrows / len(self.registed_df)

        if sample_ratio is not None:
            self.sample_nrows = sample_ratio
            
    def set_pre_encoder_load_file(self, file_name:str = './pre_encoder.json') -> None:
        self.loaded_json_path = file_name

    def get_sample_df(self, use_cache:bool = False) -> Optional[DataFrame]:
        if use_cache:
            return self.sample_df

        if self.registed_df is None:
            return None

        if self.sample_ratio is not None:
            sample_df = None
            while sample_df is None or len(sample_df) <= 10:
                print(self.sample_df)
                sample_df = self.registed_df.sample(frac=self.sample_ratio, 
                                                    random_state=self.random_seed)
                if len(sample_df) <= 10:
                    self.sample_ratio += 0.01

            return sample_df

    def __call__(self, cls: type[DataProcessor]):
        self.registed[cls.__name__] = cls()

    def get_column_names(self) -> List[str]:
        result: List[str] = []
        for col_processor in self.registed.values():
            result.append(col_processor.col_name)
        return result

    def execurate(self):
        """
        using the sample df of each column, doing some statistics and create a
        corresbonding transormfer 
        """

        if self.sample_df is None:
            self.set_sample_dataframe()

        to_save_path = open(self.loaded_json_path, 'w')
        to_save_list = []
        import ipdb;ipdb.set_trace()
        for col_name, col_processor in self.registed.items():
            processor: DataProcessor = col_processor()
            processor.run(self.registed_df, self.sample_df, to_save_list = to_save_list)
            if self.sample_df is None:
                raise ValueError("self.sample_df is None")

        json.dump(to_save_list, fp=to_save_path, cls= MyEncoder, indent=4)
        to_save_path.close()


        if self.registed_df is not None:
            result = self.registed_df.compute()
            return result

    def load_transformer_from_list(self, config_list:list[dict]):
        for config_dict in config_list:
            if 'encoder_type' in config_dict:
                pass
            pass
        pass

    def load_transformer(self, file_name:str):
        pass




