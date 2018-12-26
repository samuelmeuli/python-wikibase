from tests.constants import CLAIM_STR


class TestClaim:

    # String

    def test_string(self, item, prop):
        claims = item.claims.add(prop, CLAIM_STR)
        assert CLAIM_STR in [claim.value for claim in claims.to_list()]

    # ExternalId

    def test_external_id(self, py_wb, item, prop_external_id):
        external_id = py_wb.ExternalId().create("ID123")
        claims = item.claims.add(prop_external_id, external_id)
        assert external_id.marshal() in [claim.value.marshal() for claim in claims.to_list()]

    # GeoLocation

    def test_geo_location(self, py_wb, item, prop_geo_location):
        geo_location = py_wb.GeoLocation().create(
            latitude=1.23,
            longitude=1.23,
            precision=0.1,
            globe="http://www.wikidata.org/entity/Q2"
        )
        claims = item.claims.add(prop_geo_location, geo_location)
        assert geo_location.marshal() in [claim.value.marshal() for claim in claims.to_list()]

    # Quantity

    def test_quantity_without_unit(self, py_wb, item, prop_quantity):
        quantity = py_wb.Quantity().create(123)
        claims = item.claims.add(prop_quantity, quantity)
        assert quantity.marshal() in [claim.value.marshal() for claim in claims.to_list()]

    def test_quantity_with_unit(self, py_wb, item, prop_quantity, item_unit):
        quantity = py_wb.Quantity().create(.5, unit=item_unit)
        claims = item.claims.add(prop_quantity, quantity)
        assert quantity.marshal() in [claim.value.marshal() for claim in claims.to_list()]
