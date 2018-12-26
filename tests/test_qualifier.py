from tests.constants import QUALIFIER_STR


class TestQualifier:

    # String

    def test_string(self, claim, prop):
        qualifiers = claim.qualifiers.add(prop, QUALIFIER_STR)
        assert QUALIFIER_STR in [qualifier.value for qualifier in qualifiers.to_list()]

    # ExternalId

    def test_external_id(self, py_wb, claim, prop_external_id):
        external_id = py_wb.ExternalId().create("ID123")
        qualifiers = claim.qualifiers.add(prop_external_id, external_id)
        assert external_id.marshal() in [
            qualifier.value.marshal() for qualifier in qualifiers.to_list()
        ]

    # GeoLocation

    def test_geo_location(self, py_wb, claim, prop_geo_location):
        geo_location = py_wb.GeoLocation().create(
            latitude=1.23,
            longitude=1.23,
            precision=0.1,
            globe="http://www.wikidata.org/entity/Q2"
        )
        qualifiers = claim.qualifiers.add(prop_geo_location, geo_location)
        assert geo_location.marshal() in [
            qualifier.value.marshal() for qualifier in qualifiers.to_list()
        ]

    # Quantity

    def test_quantity_without_unit(self, py_wb, claim, prop_quantity):
        quantity = py_wb.Quantity().create(123)
        qualifiers = claim.qualifiers.add(prop_quantity, quantity)
        assert quantity.marshal() in [
            qualifier.value.marshal() for qualifier in qualifiers.to_list()
        ]

    def test_quantity_with_unit(self, py_wb, claim, prop_quantity, item_unit):
        quantity = py_wb.Quantity().create(.5, unit=item_unit)
        qualifiers = claim.qualifiers.add(prop_quantity, quantity)
        assert quantity.marshal() in [
            qualifier.value.marshal() for qualifier in qualifiers.to_list()
        ]
