from python_wikibase.data_model.entity import check_item_param
from python_wikibase.data_types.data_type import DataType


class Quantity(DataType):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.amount = None
        self.unit = None

    def unmarshal(self, data_value):
        quantity_value = data_value["value"]

        # Amount
        try:
            self.amount = int(quantity_value["amount"])
        except ValueError:
            self.amount = float(quantity_value["amount"])

        # Unit
        if quantity_value["unit"] == "1":
            # "1": No unit
            self.unit = None
        else:
            # Unit URL has the form "http://localhost:8181/entity/Q1", extract last part
            unit_item_id = quantity_value["unit"].split("/")[-1]
            self.unit = self.py_wb.Item()
            self.unit.entity_id = unit_item_id

        return self

    def marshal(self):
        marshalled = {}

        # Amount
        if self.amount >= 0:
            marshalled["amount"] = f"+{self.amount}"
        else:
            marshalled["amount"] = f"-{self.amount}"

        # Unit
        if not self.unit:
            marshalled["unit"] = "1"
        else:
            api_url = self.py_wb.api.api.base_url
            api_url_split = api_url.split("/")
            base_url = "/".join(api_url_split[:3])
            marshalled["unit"] = f"{base_url}/entity/{self.unit.entity_id}"

        return marshalled

    def create(self, amount, unit=None):
        if unit:
            check_item_param(unit, "unit")

        self.amount = amount
        self.unit = unit
        return self
