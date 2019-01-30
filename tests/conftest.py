import os

import pytest

from python_wikibase import PyWikibase
from tests.constants import (
    CLAIM_STR,
    ITEM_LABEL,
    ITEM_WITH_CLAIM_LABEL,
    LANGUAGE,
    PROP_EXTERNAL_ID_LABEL,
    PROP_GEO_LOCATION_LABEL,
    PROP_ITEM_LABEL,
    PROP_LABEL,
    PROP_QUANTITY_LABEL,
)

current_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(os.path.dirname(current_dir), "config-tests.json")


# API wrapper


@pytest.fixture(scope="session")
def py_wb():
    """Return new instance of the API wrapper with OAuth authentication"""
    try:
        return PyWikibase(config_path=config_path)
    except Exception as e:
        pytest.exit("Could not create PyWikibase class instance (with authentication): " + str(e))


# Items


@pytest.fixture(scope="function")
def item(py_wb):
    """Create a new Wikibase item, pass it to the test function, and delete it after running the
    test"""
    # Create item
    item = py_wb.Item().create(ITEM_LABEL)
    assert item.entity_id.startswith("Q")
    assert item.label.get(LANGUAGE) == ITEM_LABEL

    # Pass item to test function and wait for it to finish
    yield item

    # Delete item
    item.delete()


@pytest.fixture(scope="function")
def item_unit(py_wb):
    item_name = "Unit item"
    item = py_wb.Item().create(item_name)
    assert item.label.get(LANGUAGE) == item_name
    yield item
    item.delete()


# Properties


@pytest.fixture(scope="function")
def prop(py_wb):
    """Create a new Wikibase property (of type string), pass it to the test function, and delete it
    after running the test"""
    # Create property
    prop = py_wb.Property().create(PROP_LABEL)
    assert prop.entity_id.startswith("P")
    assert prop.label.get(LANGUAGE) == PROP_LABEL

    # Pass property to test function and wait for it to finish
    yield prop

    # Delete property
    prop.delete()


@pytest.fixture(scope="function")
def prop_external_id(py_wb):
    prop = py_wb.Property().create(PROP_EXTERNAL_ID_LABEL, data_type="ExternalId")
    assert prop.label.get(LANGUAGE) == PROP_EXTERNAL_ID_LABEL
    yield prop
    prop.delete()


@pytest.fixture(scope="function")
def prop_item(py_wb):
    prop = py_wb.Property().create(PROP_ITEM_LABEL, data_type="Item")
    assert prop.label.get(LANGUAGE) == PROP_ITEM_LABEL
    yield prop
    prop.delete()


@pytest.fixture(scope="function")
def prop_geo_location(py_wb):
    prop = py_wb.Property().create(PROP_GEO_LOCATION_LABEL, data_type="GeoLocation")
    assert prop.label.get(LANGUAGE) == PROP_GEO_LOCATION_LABEL
    yield prop
    prop.delete()


@pytest.fixture(scope="function")
def prop_quantity(py_wb):
    prop = py_wb.Property().create(PROP_QUANTITY_LABEL, data_type="Quantity")
    assert prop.label.get(LANGUAGE) == PROP_QUANTITY_LABEL
    yield prop
    prop.delete()


# Claims


@pytest.fixture(scope="function")
def claim(py_wb, prop):
    """Create a new Wikibase item with a string claim, pass the claim to the test function, and
    delete the item after running the test"""
    # Create item
    item = py_wb.Item().create(ITEM_WITH_CLAIM_LABEL)
    assert item.label.get(LANGUAGE) == ITEM_WITH_CLAIM_LABEL

    # Create claim
    claim = item.claims.add(prop, CLAIM_STR)
    assert claim.value == CLAIM_STR

    # Pass claim to test function and wait for it to finish
    yield claim

    # Delete item
    item.delete()
