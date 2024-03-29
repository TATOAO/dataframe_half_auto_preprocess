
# config.py
import DataframeHalfAutoPreprocess as dhap

@dhap.register
class col_A(dhap.DataProcessor):
    col_name = "A"
    d_type = "str"
    default_value = "missing"
    is_category = False

@dhap.register
class col_E(dhap.DataProcessor):
    col_name = "E"
    d_type = "str"
    default_value = "missing"
    is_category = False

@dhap.register
class col_B(dhap.DataProcessor):
    col_name = "B"
    d_type = "int"
    default_value = -1
    is_category = False

