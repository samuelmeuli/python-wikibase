from abc import abstractmethod

from ..base import Base
from ..data_model.entity import Item, Property


def unmarshal_data_value(py_wb, main_snak):
    # Return None if snak type is "novalue" or "somevalue"
    snak_type = main_snak["snaktype"]
    if snak_type != "value":
        return None

    # Parse and return data type if snak type is "value"
    data_type = main_snak["datatype"]
    data_value = main_snak["datavalue"]

    # Primitive data types
    if data_type in ["monolingualtext", "string"]:
        return data_value["value"]

    # DataType
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

    # Other
    elif data_type == "wikibase-item":
        item = py_wb.Item()
        item.entity_id = data_value["value"]["id"]
        return item
    elif data_type == "wikibase-property":
        prop = py_wb.Property()
        prop.entity_id = data_value["value"]["id"]
        return prop

    else:
        raise NotImplementedError


def marshal_data_type(value):
    # Primitive data types
    if type(value) == str:
        return value

    # DataType
    elif isinstance(value, DataType):
        return value.marshal()

    # Other
    elif isinstance(value, Item):
        return {"entity-type": "item", "numeric-id": int(value.entity_id[1:])}
    elif isinstance(value, Property):
        return {"entity-type": "property", "numeric-id": int(value.entity_id[1:])}

    else:
        raise NotImplementedError


class DataType(Base):
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
