class TestReference:
    """The following data types are not supported as reference values by Wikibase:

    * ExternalId
    * GeoLocation
    * Item
    """

    # No value

    def test_no_value(self, claim, prop):
        reference = claim.references.add_no_value(prop)
        assert reference.value is None

    # Some value

    def test_some_value(self, claim, prop):
        reference = claim.references.add_some_value(prop)
        assert reference.value is None

    # String

    def test_string(self, claim, prop, string_value):
        reference = claim.references.add(prop, string_value)
        assert reference.property.data_type == "StringValue"
        assert str(reference.value) == str(string_value)

    # Quantity

    def test_quantity_without_unit(self, py_wb, claim, prop_quantity):
        amount = 123
        quantity = py_wb.Quantity().create(amount)
        reference = claim.references.add(prop_quantity, quantity)
        assert reference.property.data_type == "Quantity"
        assert reference.value.amount == amount
        assert reference.value.marshal() == quantity.marshal()

    def test_quantity_without_unit_neg(self, py_wb, claim, prop_quantity):
        amount = -5
        quantity = py_wb.Quantity().create(amount)
        reference = claim.references.add(prop_quantity, quantity)
        assert reference.property.data_type == "Quantity"
        assert reference.value.amount == amount
        assert reference.value.marshal() == quantity.marshal()

    def test_quantity_with_unit(self, py_wb, claim, prop_quantity, item_unit):
        amount = 0.5
        quantity = py_wb.Quantity().create(amount, unit=item_unit)
        reference = claim.references.add(prop_quantity, quantity)
        assert reference.property.data_type == "Quantity"
        assert reference.value.amount == amount
        assert reference.value.marshal() == quantity.marshal()
