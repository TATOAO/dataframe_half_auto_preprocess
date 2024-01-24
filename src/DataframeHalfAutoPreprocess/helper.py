from json import JSONEncoder
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import numpy as np
from typing import Self, Optional
import pandas as pd

class MyEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, "__to_json__"):
            return o.__to_json__()
        else:
            return {"missing": o.__name__}
        
class LabelEncoderJson(LabelEncoder):
    uniq_name:str = "unset"
    def __init__(self, uniq_name: Optional[str]=None):
        super().__init__()
        if uniq_name == None:
            error_message = f"{self.__class__.__name__} must contains 'uniq_name' attribute"
            raise Exception(error_message)
        self.uniq_name = uniq_name

    def __to_json__(self) -> dict:
        return {
                self.uniq_name: {
                    "classes": self.classes_.tolist()
                    }
                }

    @classmethod
    def load_from_dict(cls, input_dict: dict) -> Self:
        new_obj = cls(uniq_name = input_dict['uniq_name'])
        return new_obj


class MinMaxScalerJson(MinMaxScaler):
    uniq_name:str = "unset"
    def __init__(self, uniq_name: Optional[str]=None):
        super().__init__()
        if uniq_name == None:
            error_message = f"{self.__class__.__name__} must contains 'uniq_name' attribute"
            raise Exception(error_message)
        self.uniq_name = uniq_name

    def __to_json__(self) -> dict:
        return {
                self.uniq_name: {
                        "scale": self.scale_.tolist(),
                        "min": self.min_.tolist(),
                        "data_min": self.data_min_.tolist(),
                        "data_max": self.data_max_.tolist(),
                        "data_range": self.data_range_.tolist()
                    }
                }

    @classmethod
    def load_from_dict(cls, input_dict: dict) -> Self:
        new_obj = cls()
        new_obj.scale_ = np.array(input_dict["scale"])
        new_obj.min_ = np.array(input_dict["min"])
        new_obj.data_min_ = np.array(input_dict["data_min"])
        new_obj.data_max_ = np.array(input_dict["data_max"])
        new_obj.data_range_ = np.array(input_dict["data_range"])
        return new_obj

def main():
    a = MinMaxScalerJson(uniq_name = "wefwef")
    sample_df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
    a.fit(sample_df.head(50)['A'].values.reshape(-1,1))
    a_dict = a.__to_json__()

    b = MinMaxScalerJson.load_from_dict(a_dict)
    

if __name__ == "__main__":
    main()


