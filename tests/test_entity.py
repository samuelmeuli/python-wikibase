from python_wikibase.data_model.entity import Item, Property

from .conftest import (SAMPLE_ITEM_LABEL, SAMPLE_ITEM_LABEL_2,
                       SAMPLE_PROPERTY_LABEL, SAMPLE_PROPERTY_LABEL_2)

ITEM_DESC = "Item description"
PROP_DESC = "Property description"


def test_item(wb_with_auth, item_id):
    # Get item
    item = wb_with_auth.item.get(item_id)
    assert type(item) == Item
    assert item.entity_id == item_id

    # Search for item label
    results = wb_with_auth.item.search(SAMPLE_ITEM_LABEL)
    assert results[0]["label"] == SAMPLE_ITEM_LABEL

    # Update item label
    item.set_label(SAMPLE_ITEM_LABEL_2)
    assert item.label == SAMPLE_ITEM_LABEL_2

    # Update item description
    item.set_description(ITEM_DESC)
    assert item.description == ITEM_DESC


def test_property(wb_with_auth, property_id):
    # Get property
    prop = wb_with_auth.property.get(property_id)
    assert type(prop) == Property
    assert prop.entity_id == property_id

    # Search for property label
    results = wb_with_auth.property.search(SAMPLE_PROPERTY_LABEL)
    assert results[0]["label"] == SAMPLE_PROPERTY_LABEL

    # Update property label
    prop.set_label(SAMPLE_PROPERTY_LABEL_2)
    assert prop.label == SAMPLE_PROPERTY_LABEL_2

    # Update property description
    prop.set_description(PROP_DESC)
    assert prop.description == PROP_DESC
