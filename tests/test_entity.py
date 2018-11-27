from python_wikibase.data_model.entity import Item, Property

from .conftest import (SAMPLE_ITEM_LABEL, SAMPLE_ITEM_LABEL_2,
                       SAMPLE_PROPERTY_LABEL)


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

def test_property(wb_with_auth, property_id):
    # Get property
    prop = wb_with_auth.property.get(property_id)
    assert type(prop) == Property
    assert prop.entity_id == property_id

    # Search for property label
    results = wb_with_auth.property.search(SAMPLE_PROPERTY_LABEL)
    assert results[0]["label"] == SAMPLE_PROPERTY_LABEL
