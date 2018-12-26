from tests.constants import REFERENCE_STR


# The following data types are not supported as reference values by Wikibase:
# - ExternalId
# - GeoLocation

class TestReference:

    # String

    def test_string(self, claim, prop):
        references = claim.references.add(prop, REFERENCE_STR)
        assert REFERENCE_STR in [reference.value for reference in references.to_list()]

    # Quantity

    def test_quantity_without_unit(self, py_wb, claim, prop_quantity):
        quantity = py_wb.Quantity().create(123)
        references = claim.references.add(prop_quantity, quantity)
        assert quantity.marshal() in [
            reference.value.marshal() for reference in references.to_list()
        ]

    def test_quantity_with_unit(self, py_wb, claim, prop_quantity, item_unit):
        quantity = py_wb.Quantity().create(.5, unit=item_unit)
        references = claim.references.add(prop_quantity, quantity)
        assert quantity.marshal() in [
            reference.value.marshal() for reference in references.to_list()
        ]
