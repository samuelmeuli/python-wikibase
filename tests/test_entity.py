from python_wikibase.data_model.entity import Item, Property

from .conftest import (SAMPLE_ITEM_LABEL, SAMPLE_ITEM_LABEL_2,
                       SAMPLE_PROPERTY_LABEL, SAMPLE_PROPERTY_LABEL_2)

ITEM_DESC = "Item description"
ITEM_ALIAS = "Item alias"
PROP_DESC = "Property description"
PROP_ALIAS = "Property alias"


def test_item(wb_with_auth, item_id):
    # Get item
    item = wb_with_auth.item.get(item_id)
    assert type(item) == Item
    assert item.entity_id == item_id

    # Search for item label
    results = wb_with_auth.item.search(SAMPLE_ITEM_LABEL)
    assert results[0]["label"] == SAMPLE_ITEM_LABEL

    # Update item label
    item.label.set(SAMPLE_ITEM_LABEL_2)
    assert item.label.get() == SAMPLE_ITEM_LABEL_2

    # Update item description
    item.description.set(ITEM_DESC)
    assert item.description.get() == ITEM_DESC

    # Update item aliases
    item.aliases.add(ITEM_ALIAS)
    assert ITEM_ALIAS in item.aliases.get()
    item.aliases.remove(ITEM_ALIAS)
    assert ITEM_ALIAS not in item.aliases.get()


def test_property(wb_with_auth, property_id):
    # Get property
    prop = wb_with_auth.property.get(property_id)
    assert type(prop) == Property
    assert prop.entity_id == property_id

    # Search for property label
    results = wb_with_auth.property.search(SAMPLE_PROPERTY_LABEL)
    assert results[0]["label"] == SAMPLE_PROPERTY_LABEL

    # Update property label
    prop.label.set(SAMPLE_PROPERTY_LABEL_2)
    assert prop.label.get() == SAMPLE_PROPERTY_LABEL_2

    # Update property description
    prop.description.set(PROP_DESC)
    assert prop.description.get() == PROP_DESC

    # Update property aliases
    prop.aliases.add(PROP_ALIAS)
    assert PROP_ALIAS in prop.aliases.get()
    prop.aliases.remove(PROP_ALIAS)
    assert PROP_ALIAS not in prop.aliases.get()
