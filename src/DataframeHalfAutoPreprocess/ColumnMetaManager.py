from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from typing import Optional


class ColumnMeta():
    col_name: str
    is_categorical: bool
    # categorical_meta: Optional[dict]
    # numarical_meta: Optional[dict]
    min: Optional[float]
    max: Optional[float]
    counts: Optional[dict]



class ColumnMetaManager():

    def save_column_meta(self):
        pass

    def load_column_meta(self):
        """TODO: Docstring for load_column_meta.
        :returns: TODO

        """
        pass
