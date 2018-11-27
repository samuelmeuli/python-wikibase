import os

import pytest
from python_wikibase import Wikibase

current_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(os.path.dirname(current_dir), "config-tests.json")

SAMPLE_ITEM_LABEL = "Test item"
SAMPLE_ITEM_LABEL_2 = "Test item 2"
SAMPLE_PROPERTY_LABEL = "Test property"
SAMPLE_PROPERTY_LABEL_2 = "Test property 2"


@pytest.fixture(scope="session")
def wb_without_auth():
    """Return new instance of the API wrapper without authentication
    :return: API wrapper class
    :rtype: Wikibase
    """
    try:
        return Wikibase()
    except Exception as e:
        pytest.exit("Could not create Wikibase class instance (without authentication): " + str(e))


@pytest.fixture(scope="session")
def wb_with_auth():
    """Return new instance of the API wrapper with OAuth authentication
    :return: API wrapper class
    :rtype: Wikibase
    """
    try:
        return Wikibase(config_path=config_path)
    except Exception as e:
        pytest.exit("Could not create Wikibase class instance (with authentication): " + str(e))


@pytest.fixture(scope="function")
def item_id(wb_with_auth):
    """Create a new Wikibase item and delete it after running the test

    :param wb_with_auth: API wrapper class (authenticated)
    :type wb_with_auth: Wikibase
    :return: Yield the item's ID
    :rtype: str
    """
    # Create item
    item = wb_with_auth.item.create(SAMPLE_ITEM_LABEL)
    assert item.entity_id.startswith("Q")
    assert item.label == SAMPLE_ITEM_LABEL

    # Pass entity_id to test function and wait for it to finish
    yield item.entity_id

    # Delete item
    item.delete()


@pytest.fixture(scope="function")
def property_id(wb_with_auth):
    """Create a new Wikibase property (of type string) and delete it after running the test

    :param wb_with_auth: API wrapper class (authenticated)
    :type wb_with_auth: Wikibase
    :return: Yield the property's ID
    :rtype: str
    """
    # Create property
    prop = wb_with_auth.property.create(SAMPLE_PROPERTY_LABEL, "string")
    assert prop.entity_id.startswith("P")
    assert prop.label == SAMPLE_PROPERTY_LABEL

    # Pass entity_id to test function and wait for it to finish
    yield prop.entity_id

    # Delete property
    prop.delete()
