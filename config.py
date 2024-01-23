from utils import register
from DataProcessor import DataProcessor


@register.register
class col_A(DataProcessor):
    col_name = "A"
    d_type = "int"
    default_value = -1
    is_category = False
