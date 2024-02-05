from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from typing import Optional, Any
import json
from abc import ABC, abstractmethod

class BaseModel(ABC):
    def to_dict(self):
        """
        Convert instance to dictionary, including only properties that do not start with an underscore.
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    @classmethod
    def from_dict(cls, adict):
        """
        Create an instance of cls from a dictionary.
        """
        instance = cls()
        for k, v in adict.items():
            setattr(instance, k, v)
        return instance

class ClassManager:
    @staticmethod
    def save(instance, filename):
        """
        Save an instance of a class derived from BaseModel to a JSON file.
        """
        with open(filename, 'w') as file:
            json.dump(instance.to_dict(), file, indent=4)

    @staticmethod
    def load(class_initiator: BaseModel, filename):
        """
        Load an instance of a class derived from BaseModel from a JSON file.
        """
        with open(filename, 'r') as file:
            adict = json.load(file)
        return class_initiator.from_dict(adict)

class LabelEncoderJson(LabelEncoder):

    def toJSON(self):
        return json.dumps(self, default=lambda x: "shit")



class ColumnMeta(BaseModel):
    col_name: str
    is_categorical: bool
    # categorical_meta: Optional[dict]
    # numarical_meta: Optional[dict]
    min: Optional[float]
    max: Optional[float]
    counts: Optional[dict]

def main():

    bb = LabelEncoderJson()
    records = {"a": bb}
    file = open('a.json', 'w')
    # json.dump(records, file)
    print("ssss")
    file.close()

    

if __name__ == "__main__":
    main()



