from json import JSONEncoder
# from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from dask_ml.preprocessing import MinMaxScaler, OrdinalEncoder, LabelEncoder
import numpy as np
from typing import Optional
import sys

# to adapt newer version of python
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import json
import pandas as pd


class MyEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, "__to_json__"):
            return o.__to_json__()
        else:
            return None
        
class OrdinalEncoderJson(OrdinalEncoder):
    column_name:str = "unset"
    def __init__(self, encoder_id: Optional[str]=None, **kargs):
        super().__init__(**kargs)
        if encoder_id == None:
            error_message = f"{self.__class__.__name__} must contains 'encoder_id' attribute"
            raise Exception(error_message)
        self.column_name = encoder_id


    def get_categories(self) -> list:
        return self.dtypes_[self.column_name].categories.tolist()

    def __to_json__(self) -> dict:
        return {
                    "encoder_id": self.column_name,
                    "encoder_type": "OrdinalEncoder",
                    "classes": self.get_categories()
                }

    @classmethod
    def load_from_dict(cls, input_dict: dict) -> Self:

        if input_dict['encoder_type'] != "OrdinalEncoder":
            error_message = (f"Encoder Type {input_dict['encoder_type']}(input)",
                             f"Not Match {cls.__name__}")
            raise(Exception(error_message))

        new_obj = cls(encoder_id = input_dict['encoder_id'])
        column_name = input_dict['encoder_id']
        # new_obj.fit(np.array(input_dict['classes']).reshape(-1,1))
        fake_df = pd.DataFrame({column_name: input_dict['classes']})
        fake_df[column_name] = fake_df[column_name].astype('category')
        new_obj.fit(fake_df)
        return new_obj

    def __repr__(self):
        return str(self.__dict__)

class LabelEncoderJson(LabelEncoder):
    encdoer_id:str = "unset"
    def __init__(self, encoder_id: Optional[str]=None):
        super().__init__()
        if encoder_id == None:
            error_message = f"{self.__class__.__name__} must contains 'encoder_id' attribute"
            raise Exception(error_message)
        self.encoder_id = encoder_id

    def __to_json__(self) -> dict:
        return {
                    "encoder_id": self.encoder_id,
                    "encoder_type": "LabelEncoder",
                    "classes": self.classes_.tolist()
                }

    @classmethod
    def load_from_dict(cls, input_dict: dict) -> Self:
        """
        example dict:
            {
                "encoder_id": "AAA_encoder",
                "encoder_type": "MinMaxScaler",
                "scale": [12,24,4,34],
                "min": [11,2,4,5],
                "data_min": self.data_min_.tolist(),
                "data_max": self.data_max_.tolist(),
                "data_range": self.data_range_.tolist()
            }

        """

        if input_dict['encoder_type'] != "LabelEncoder":
            error_message = (f"Encoder Type {input_dict['encoder_type']}(input)",
                             f"Not Match {cls.__name__}")
            raise(Exception(error_message))

        new_obj = cls(encoder_id = input_dict['encoder_id'])
        new_obj.classes_ = np.array(input_dict['classes'])
        return new_obj


class MinMaxScalerJson(MinMaxScaler):
    encoder_id:str = "unset"
    def __init__(self, encoder_id: Optional[str]=None):
        super().__init__()
        if encoder_id == None:
            error_message = f"{self.__class__.__name__} must contains 'encoder_id' attribute"
            raise Exception(error_message)
        self.encoder_id = encoder_id

    def __to_json__(self) -> dict:
        return {
                    "encoder_id": self.encoder_id,
                    "encoder_type": "MinMaxScaler",
                    "scale": self.scale_.tolist(),
                    "min": self.min_.tolist(),
                    "data_min": self.data_min_.tolist(),
                    "data_max": self.data_max_.tolist(),
                    "data_range": self.data_range_.tolist()
                }

    @classmethod
    def load_from_dict(cls, input_dict: dict) -> Self:
        """
        example dict:
            {
                "encoder_id": "AAA_encoder",
                "encoder_type": "MinMaxScaler",
                "scale": [12,24,4,34],
                "min": [11,2,4,5],
                "data_min": self.data_min_.tolist(),
                "data_max": self.data_max_.tolist(),
                "data_range": self.data_range_.tolist()
            }

        """
        if input_dict['encoder_type'] != "MinMaxScaler":
            error_message = (f"Encoder Type {input_dict['encoder_type']}(input)",
                             f"Not Match {cls.__name__}")
            raise(Exception(error_message))


        new_obj = cls(input_dict['encoder_id'])
        new_obj.scale_ = np.array(input_dict["scale"])
        new_obj.min_ = np.array(input_dict["min"])
        new_obj.data_min_ = np.array(input_dict["data_min"])
        new_obj.data_max_ = np.array(input_dict["data_max"])
        new_obj.data_range_ = np.array(input_dict["data_range"])
        return new_obj

def main():
    # example_min_max_saler()
    example_label_encoder()
    # example_ordinal_encoder()

def example_label_encoder():
    a = LabelEncoderJson(encoder_id = "wefwef")
    sample_df = pd.DataFrame(np.random.choice(list("abcd"), size=(100,4)), columns=list('ABCD'))
    a.fit(sample_df.head(50)['A'])
    # a_dict = a.__to_json__()

    file = open('a.json', 'w')
    j_s = json.dump(a, fp = file, cls=MyEncoder)
    file.close()


    file = open('a.json', 'r')
    the_dict = json.load(fp = file)
    file.close()

    b = LabelEncoderJson.load_from_dict(the_dict)
    x = sample_df.tail(50)['A']
    print(x[:5])
    x1 = b.transform(x)
    print(x1[:5])
    pass

def example_ordinal_encoder():
    a = OrdinalEncoderJson(encoder_id = "wefwef")
    np.random.seed(10)
    sample_df = pd.DataFrame(np.random.choice(list("abcd"), size=(100,4)), columns=list('ABCD'))

    a.fit(sample_df.head(50)['A'].values.reshape(-1,1))

    # a_dict = a.__to_json__()
    file = open('a.json', 'w')
    j_s = json.dump(a, fp = file, cls=MyEncoder)
    file.close()


    file = open('a.json', 'r')
    the_dict = json.load(fp = file)
    file.close()
    b = OrdinalEncoderJson.load_from_dict(the_dict)
    
    file.close()



    sample_df = pd.DataFrame(np.random.choice(list("cdef"), size=(100,4)), columns=list('ABCD'))
    x = sample_df.tail(50)['A'].values.reshape(-1,1)
    print(x[:10])
    x1 = b.transform(x)
    print(x1[:10])
    pass

def example_min_max_saler():
    a = MinMaxScalerJson(encoder_id = "wefwef")
    sample_df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
    a.fit(sample_df.head(50)['A'].values.reshape(-1,1))
    # a_dict = a.__to_json__()

    file = open('a.json', 'w')
    j_s = json.dump(a, fp = file, cls=MyEncoder)
    file.close()


    file = open('a.json', 'r')
    the_dict = json.load(fp = file)
    file.close()


    b = MinMaxScalerJson.load_from_dict(the_dict)
    x = sample_df.tail(50)['A'].values.reshape(-1,1)
    print(x[:5])
    x1 = b.transform(x)
    print(x1[:5])
    

if __name__ == "__main__":
    main()


