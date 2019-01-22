from tests.constants import QUALIFIER_STR


class TestQualifier:

    # No value

    def test_no_value(self, claim, prop):
        qualifier = claim.qualifiers.add_no_value(prop)
        assert qualifier.value is None

    # Some value

    def test_some_value(self, claim, prop):
        qualifier = claim.qualifiers.add_some_value(prop)
        assert qualifier.value is None

    # String

    def test_string(self, claim, prop):
        qualifier = claim.qualifiers.add(prop, QUALIFIER_STR)
        assert qualifier.value == QUALIFIER_STR

    # Item

    def test_item(self, py_wb, claim, prop_item):
        item_2 = py_wb.Item().create("Item 2")
        qualifier = claim.qualifiers.add(prop_item, item_2)
        assert qualifier.value.entity_id == item_2.entity_id

    # ExternalId

    def test_external_id(self, py_wb, claim, prop_external_id):
        external_id = py_wb.ExternalId().create("ID123")
        qualifier = claim.qualifiers.add(prop_external_id, external_id)
        assert qualifier.value.marshal() == external_id.marshal()

    # GeoLocation

    def test_geo_location(self, py_wb, claim, prop_geo_location):
        geo_location = py_wb.GeoLocation().create(
            latitude=1.23,
            longitude=1.23,
            precision=0.1,
            globe="http://www.wikidata.org/entity/Q2"
        )
        qualifier = claim.qualifiers.add(prop_geo_location, geo_location)
        assert qualifier.value.marshal() == geo_location.marshal()

    # Quantity

    def test_quantity_without_unit(self, py_wb, claim, prop_quantity):
        quantity = py_wb.Quantity().create(123)
        qualifier = claim.qualifiers.add(prop_quantity, quantity)
        assert qualifier.value.marshal() == quantity.marshal()

    def test_quantity_with_unit(self, py_wb, claim, prop_quantity, item_unit):
        quantity = py_wb.Quantity().create(.5, unit=item_unit)
        qualifier = claim.qualifiers.add(prop_quantity, quantity)
        assert qualifier.value.marshal() == quantity.marshal()
