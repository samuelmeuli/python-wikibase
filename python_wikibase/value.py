from python_wikibase.base import Base


class Value(Base):
    def __init__(self, py_wb, wb, language):
        super().__init__(py_wb, wb, language)


def check_value_param(value, param_name="value"):
    if not isinstance(value, Value):
        raise ValueError(f'"{param_name}" parameter must be instance of Entity or DataType class')
