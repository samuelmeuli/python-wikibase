from .conftest import (
    LANGUAGE,
    SAMPLE_ITEM_LABEL,
    SAMPLE_ITEM_LABEL_2,
    SAMPLE_PROPERTY_LABEL,
)

ITEM_DESC = "Item description"
ITEM_ALIAS = "Item alias"
PROP_DESC = "Property description"
PROP_ALIAS = "Property alias"


def test_item(py_wb, item_id):
    # Get item
    item = py_wb.Item().get(item_id)
    assert item.entity_id == item_id
    assert item.label.get(LANGUAGE) == SAMPLE_ITEM_LABEL

    # Update item label
    item.label.set(SAMPLE_ITEM_LABEL_2)
    assert item.label.get(LANGUAGE) == SAMPLE_ITEM_LABEL_2

    # Update item description
    item.description.set(ITEM_DESC)
    assert item.description.get() == ITEM_DESC

    # Update item aliases
    item.aliases.add(ITEM_ALIAS)
    assert ITEM_ALIAS in item.aliases.get()
    item.aliases.remove(ITEM_ALIAS)
    assert ITEM_ALIAS not in item.aliases.get()


def test_property(py_wb, property_id):
    # Get property
    prop = py_wb.Property().get(property_id)
    assert prop.entity_id == property_id
    assert prop.label.get(LANGUAGE) == SAMPLE_PROPERTY_LABEL
