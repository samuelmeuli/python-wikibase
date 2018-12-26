from tests.constants import CLAIM_STR


class TestClaim:

    # String

    def test_string(self, item, prop):
        claim = item.claims.add(prop, CLAIM_STR)
        assert claim.value == CLAIM_STR

    # ExternalId

    def test_external_id(self, py_wb, item, prop_external_id):
        external_id = py_wb.ExternalId().create("ID123")
        claim = item.claims.add(prop_external_id, external_id)
        assert claim.value.marshal() == external_id.marshal()

    # GeoLocation

    def test_geo_location(self, py_wb, item, prop_geo_location):
        geo_location = py_wb.GeoLocation().create(
            latitude=1.23,
            longitude=1.23,
            precision=0.1,
            globe="http://www.wikidata.org/entity/Q2"
        )
        claim = item.claims.add(prop_geo_location, geo_location)
        assert claim.value.marshal() == geo_location.marshal()

    # Quantity

    def test_quantity_without_unit(self, py_wb, item, prop_quantity):
        quantity = py_wb.Quantity().create(123)
        claim = item.claims.add(prop_quantity, quantity)
        assert claim.value.marshal() == quantity.marshal()

    def test_quantity_with_unit(self, py_wb, item, prop_quantity, item_unit):
        quantity = py_wb.Quantity().create(.5, unit=item_unit)
        claim = item.claims.add(prop_quantity, quantity)
        assert claim.value.marshal() == quantity.marshal()
