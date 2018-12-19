import pytest

from tests.conftest import LANGUAGE


@pytest.fixture(scope="function")
def external_id_prop(py_wb):
    prop_name = "Catalog ID"
    prop = py_wb.Property().create(prop_name, property_type="ExternalId")
    assert prop.label.get(LANGUAGE) == prop_name
    yield prop
    prop.delete()


@pytest.fixture(scope="function")
def geo_location_prop(py_wb):
    prop_name = "Location"
    prop = py_wb.Property().create(prop_name, property_type="GeoLocation")
    assert prop.label.get(LANGUAGE) == prop_name
    yield prop
    prop.delete()


class TestClaim:
    def test_external_id(self, py_wb, item_id, external_id_prop):
        item = py_wb.Item().get(entity_id=item_id)
        external_id = py_wb.ExternalId().create("Q1")
        claims = item.claims.add(external_id_prop, external_id)
        assert external_id.marshal() in [claim.value.marshal() for claim in claims.to_list()]

    def test_geo_location(self, py_wb, item_id, geo_location_prop):
        item = py_wb.Item().get(entity_id=item_id)
        geo_location = py_wb.GeoLocation().create(
            latitude=1.23,
            longitude=1.23,
            precision=0.1,
            globe="http://www.wikidata.org/entity/Q2"
        )
        claims = item.claims.add(geo_location_prop, geo_location)
        assert geo_location.marshal() in [claim.value.marshal() for claim in claims.to_list()]
