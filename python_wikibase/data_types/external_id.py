from python_wikibase.data_types.data_type import DataType


class ExternalId(DataType):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.external_id = None

    def __str__(self):
        return self.external_id

    def unmarshal(self, data_value):
        self.external_id = data_value["value"]
        return self

    def marshal(self):
        return self.external_id

    def create(self, external_id):
        self.external_id = external_id
        return self
