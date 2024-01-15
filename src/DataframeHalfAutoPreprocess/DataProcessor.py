from typing import Any, Optional, List
from pandas import DataFrame
from multiprocessing import Pool

class DataProcessor:
    from_cols: List[Optional[str]] = []
    col_name: str = ""
    d_type: str = ""
    default_value: Optional[Any] = None
    is_category: bool = True

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self

    def process(self, df: DataFrame):


        if self.default_value:
            # dask is not allow "inplace"
            df[self.col_name] = df[self.col_name].fillna(self.default_value)
        # if is_category:
        #     df[self.col_name] = df[self.col_name].astype(self.d_type)
        df[self.col_name] = df[self.col_name].astype(self.d_type)


    def statistic(self, df: DataFrame):
        """
        mission value ratio
        distribution
        """
        # with Pool() as pool:
        pass

    def run(self, df: DataFrame):
        self.process(df)
        self.statistic(df)

    def __init_subclass__(cls, **kwargs):
        """
        Ensure the subclas must contains non emptry string
        """
        for required in ('col_name', 'd_type'):
            if getattr(cls, required) == "":
                raise TypeError(f"Can't instantiate abstract class {cls.__name__} without {required} attribute defined")
        
        return super().__init_subclass__(**kwargs)

