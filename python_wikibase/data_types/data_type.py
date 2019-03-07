from abc import abstractmethod

from python_wikibase.value import Value


class DataType(Value):
    """Abstract class for Wikibase data types (see
    https://www.mediawiki.org/wiki/Wikibase/DataModel)"""

    @abstractmethod
    def unmarshal(self, data_value):
        pass

    @abstractmethod
    def marshal(self):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass


def unmarshal_data_value(py_wb, main_snak):
    # Return None if snak type is "novalue" or "somevalue"
    snak_type = main_snak["snaktype"]
    if snak_type != "value":
        return None

    if "datatype" in main_snak:
        data_type = main_snak["datatype"]
    else:
        data_type = "string"
    data_value = main_snak["datavalue"]

    # DataType
    if data_type in ["monolingualtext", "string"]:
        return py_wb.StringValue().unmarshal(data_value)
    elif data_type == "commonsMedia":
        raise NotImplementedError  # TODO
    elif data_type == "external-id":
        return py_wb.ExternalId().unmarshal(data_value)
    elif data_type == "geo-shape":
        raise NotImplementedError  # TODO
    elif data_type == "globe-coordinate":
        return py_wb.GeoLocation().unmarshal(data_value)
    elif data_type == "math":
        raise NotImplementedError  # TODO
    elif data_type == "quantity":
        return py_wb.Quantity().unmarshal(data_value)
    elif data_type == "tabular-data":
        raise NotImplementedError  # TODO
    elif data_type == "time":
        raise NotImplementedError  # TODO
    elif data_type == "url":
        raise NotImplementedError  # TODO
    elif data_type == "wikibase-form":
        raise NotImplementedError  # TODO
    elif data_type == "wikibase-lexeme":
        raise NotImplementedError  # TODO
    elif data_type == "wikibase-sense":
        raise NotImplementedError  # TODO

    # Entity
    elif data_type == "wikibase-item":
        item = py_wb.Item()
        item.entity_id = data_value["value"]["id"]
        return item
    elif data_type == "wikibase-property":
        prop = py_wb.Property()
        prop.entity_id = data_value["value"]["id"]
        return prop

    else:
        raise NotImplementedError(f'No unmarshalling function for data type "{data_type}" defined')


def check_data_type(value, prop):
    """Check if value is of correct data type

    :param value: Value whose data type shall be checked
    :type value: Value
    :param prop: Property whose data type the value shall be compared with
    :type prop: Property
    """
    data_type = value.__class__.__name__
    if data_type != prop.data_type:
        raise ValueError(f"Value must be instance of {prop.data_type} class")
