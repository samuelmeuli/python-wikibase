import pytest

from tests.conftest import LANGUAGE


@pytest.fixture(scope="function")
def external_id_prop(py_wb):
    prop_name = "ExternalId prop"
    prop = py_wb.Property().create(prop_name, property_type="ExternalId")
    assert prop.label.get(LANGUAGE) == prop_name
    yield prop
    prop.delete()


@pytest.fixture(scope="function")
def geo_location_prop(py_wb):
    prop_name = "GeoLocation prop"
    prop = py_wb.Property().create(prop_name, property_type="GeoLocation")
    assert prop.label.get(LANGUAGE) == prop_name
    yield prop
    prop.delete()


@pytest.fixture(scope="function")
def quantity_prop(py_wb):
    prop_name = "Quantity prop"
    prop = py_wb.Property().create(prop_name, property_type="Quantity")
    assert prop.label.get(LANGUAGE) == prop_name
    yield prop
    prop.delete()


@pytest.fixture(scope="function")
def quantity_unit_item(py_wb):
    item_name = "Unit item"
    item = py_wb.Item().create(item_name)
    assert item.label.get(LANGUAGE) == item_name
    yield item
    item.delete()


class TestClaim:

    # ExternalId

    def test_external_id(self, py_wb, item_id, external_id_prop):
        item = py_wb.Item().get(entity_id=item_id)
        external_id = py_wb.ExternalId().create("Q1")
        claims = item.claims.add(external_id_prop, external_id)
        assert external_id.marshal() in [claim.value.marshal() for claim in claims.to_list()]

    # GeoLocation

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

    # Quantity

    def test_quantity_without_unit(self, py_wb, item_id, quantity_prop):
        item = py_wb.Item().get(entity_id=item_id)
        quantity = py_wb.Quantity().create(123)
        claims = item.claims.add(quantity_prop, quantity)
        assert quantity.marshal() in [claim.value.marshal() for claim in claims.to_list()]

    def test_quantity_with_unit(self, py_wb, item_id, quantity_prop, quantity_unit_item):
        item = py_wb.Item().get(entity_id=item_id)
        quantity = py_wb.Quantity().create(.5, unit=quantity_unit_item)
        claims = item.claims.add(quantity_prop, quantity)
        assert quantity.marshal() in [claim.value.marshal() for claim in claims.to_list()]
