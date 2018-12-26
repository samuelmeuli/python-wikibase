from tests.constants import REFERENCE_STR


# The following data types are not supported as reference values by Wikibase:
# - ExternalId
# - GeoLocation

class TestReference:

    # String

    def test_string(self, claim, prop):
        reference = claim.references.add(prop, REFERENCE_STR)
        assert reference.value == REFERENCE_STR

    # Quantity

    def test_quantity_without_unit(self, py_wb, claim, prop_quantity):
        quantity = py_wb.Quantity().create(123)
        reference = claim.references.add(prop_quantity, quantity)
        assert reference.value.marshal() == quantity.marshal()

    def test_quantity_with_unit(self, py_wb, claim, prop_quantity, item_unit):
        quantity = py_wb.Quantity().create(.5, unit=item_unit)
        reference = claim.references.add(prop_quantity, quantity)
        assert reference.value.marshal() == quantity.marshal()
