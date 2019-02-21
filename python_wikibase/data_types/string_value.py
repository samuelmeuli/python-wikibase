from python_wikibase.data_types.data_type import DataType


class StringValue(DataType):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.value = None

    def __str__(self):
        return self.value

    def unmarshal(self, data_value):
        self.value = data_value["value"]
        return self

    def marshal(self):
        return self.value

    def create(self, value):
        self.value = value
        return self
