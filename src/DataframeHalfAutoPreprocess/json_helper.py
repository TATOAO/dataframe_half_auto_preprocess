from typing import List, Union, Dict
from .helper import MinMaxScalerJson, OrdinalEncoderJson, MyEncoder
import json

__all___ = "json_saver"

class JsonSaverHelper:
    model_map: Dict[str,Union[MinMaxScalerJson, OrdinalEncoderJson]] = {}
    json_file_path: str

    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def add_model(self, col_name:str, model:Union[MinMaxScalerJson, OrdinalEncoderJson]):
        self.model_map[col_name] = model

    def set_json_file_path(self, path:str):
        self.json_file_path = path

    def write_to_json(self, json_file: str) -> None:
        """
        save the whole model configs into json
        """
        f = open(json_file, 'w')
        json.dump(self.model_map, fp=f, cls= MyEncoder, indent=4)
        f.close()

    def get_encoder(self, encoder_name: str) -> Union[MinMaxScalerJson, OrdinalEncoderJson]:
        if len(self.model_map) == 0:
            self.load_transformer_from_file(self.json_file_path)
        return self.model_map[encoder_name]

    def load_transformer_from_file(self, load_path:str = ""):
        file = open(load_path, 'r')
        config_list = json.load(file)
        file.close()
        self.load_transformer_from_list(config_list)

    def load_transformer_from_list(self, config_list:list[dict]) -> None:

        for config_dict in config_list.values():
            if 'encoder_type' not in config_dict:
                raise Exception("The source json file has no encoder_type")
            
            col_name = config_dict['encoder_id']
            if config_dict['encoder_type'] == "MinMaxScaler":
                self.model_map[col_name] = MinMaxScalerJson.\
                                        load_from_dict(config_dict)
            elif config_dict['encoder_type'] == "OrdinalEncoder":

                self.model_map[col_name] = OrdinalEncoderJson.\
                                        load_from_dict(config_dict)

            else:
                raise Exception("Now only support MinMaxScaler and OrdinalEncoder")

# json_saver = JsonSaverHelper()
