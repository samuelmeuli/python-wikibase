class TestClaim:

    # No value

    def test_no_value(self, item, prop):
        claim = item.claims.add_no_value(prop)
        assert claim.value is None

    # Some value

    def test_some_value(self, item, prop):
        claim = item.claims.add_some_value(prop)
        assert claim.value is None

    # String

    def test_string(self, item, prop, string_value):
        claim = item.claims.add(prop, string_value)
        assert claim.property.data_type == "StringValue"
        assert str(claim.value) == string_value.value

    # Item

    def test_item(self, py_wb, item, prop_item):
        item_2 = py_wb.Item().create("Item 2")
        claim = item.claims.add(prop_item, item_2)
        assert claim.property.data_type == "Item"
        assert claim.value.entity_id == item_2.entity_id

    # ExternalId

    def test_external_id(self, py_wb, item, prop_external_id):
        external_id = py_wb.ExternalId().create("ID123")
        claim = item.claims.add(prop_external_id, external_id)
        assert claim.property.data_type == "ExternalId"
        assert claim.value.external_id == external_id.external_id
        assert str(claim.value) == external_id.external_id
        assert claim.value.marshal() == external_id.marshal()

    # GeoLocation

    def test_geo_location(self, py_wb, item, prop_geo_location):
        geo_location = py_wb.GeoLocation().create(
            1.23,
            4.56,
            precision=0.1,
            globe="http://www.wikidata.org/entity/Q2"
        )
        claim = item.claims.add(prop_geo_location, geo_location)
        assert claim.property.data_type == "GeoLocation"
        assert claim.value.marshal() == geo_location.marshal()

    # Quantity

    def test_quantity_without_unit(self, py_wb, item, prop_quantity):
        amount = 123
        quantity = py_wb.Quantity().create(amount)
        claim = item.claims.add(prop_quantity, quantity)
        assert claim.property.data_type == "Quantity"
        assert claim.value.amount == amount
        assert int(claim.value) == amount
        assert claim.value.marshal() == quantity.marshal()

    def test_quantity_without_unit_neg(self, py_wb, item, prop_quantity):
        amount = -5
        quantity = py_wb.Quantity().create(amount)
        claim = item.claims.add(prop_quantity, quantity)
        assert claim.property.data_type == "Quantity"
        assert claim.value.amount == amount
        assert int(claim.value) == amount
        assert claim.value.marshal() == quantity.marshal()

    def test_quantity_with_unit(self, py_wb, item, prop_quantity, item_unit):
        amount = 0.5
        quantity = py_wb.Quantity().create(amount, unit=item_unit)
        claim = item.claims.add(prop_quantity, quantity)
        assert claim.property.data_type == "Quantity"
        assert claim.value.amount == amount
        assert float(claim.value) == amount
        assert claim.value.marshal() == quantity.marshal()
