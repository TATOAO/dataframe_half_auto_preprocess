
# config.py
import DataframeHalfAutoPreprocess as dhap

@dhap.register
class col_A(dhap.DataProcessor):
    col_name = "A"
    d_type = "str"
    default_value = "missing"
    is_category = False

    def statistic(self, df):
        super().statistic(df)
        pass
