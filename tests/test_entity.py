from tests.constants import ITEM_ALIAS, ITEM_DESC, ITEM_LABEL, ITEM_LABEL_2, LANGUAGE, PROP_LABEL


class TestEntity:
    def test_item(self, py_wb, item):
        # Get item
        item_fetched = py_wb.Item().get(entity_id=item.entity_id)
        assert item_fetched.entity_id == item.entity_id
        assert item_fetched.label.get(LANGUAGE) == ITEM_LABEL

        # Update item label
        item_fetched.label.set(ITEM_LABEL_2)
        assert item_fetched.label.get(LANGUAGE) == ITEM_LABEL_2

        # Update item description
        item_fetched.description.set(ITEM_DESC)
        assert item_fetched.description.get() == ITEM_DESC

        # Update item aliases
        item_fetched.aliases.add(ITEM_ALIAS)
        assert ITEM_ALIAS in item_fetched.aliases.get()
        item_fetched.aliases.remove(ITEM_ALIAS)
        assert ITEM_ALIAS not in item_fetched.aliases.get()

    def test_property(self, py_wb, prop):
        # Get property
        prop_fetched = py_wb.Property().get(entity_id=prop.entity_id)
        assert prop_fetched.entity_id == prop.entity_id
        assert prop_fetched.label.get(LANGUAGE) == PROP_LABEL
