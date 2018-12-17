import os

import pytest

from python_wikibase import PyWikibase

current_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(os.path.dirname(current_dir), "config-tests.json")

LANGUAGE = "en"
SAMPLE_ITEM_LABEL = "Test item"
SAMPLE_ITEM_LABEL_2 = "Test item 2"
SAMPLE_PROPERTY_LABEL = "Test property"


@pytest.fixture(scope="session")
def py_wb():
    """Return new instance of the API wrapper with OAuth authentication

    :return: API wrapper class
    :rtype: Wikibase
    """
    try:
        return PyWikibase(config_path=config_path)
    except Exception as e:
        pytest.exit("Could not create PyWikibase class instance (with authentication): " + str(e))


@pytest.fixture(scope="function")
def item_id(py_wb):
    """Create a new Wikibase item and delete it after running the test

    :param py_wb: API wrapper class
    :type py_wb: PyWikibase
    :return: Yield the property's ID
    :rtype: str
    """
    # Create item
    item = py_wb.Item().create(SAMPLE_ITEM_LABEL)
    assert item.entity_id.startswith("Q")
    assert item.label.get(LANGUAGE) == SAMPLE_ITEM_LABEL

    # Pass entity_id to test function and wait for it to finish
    yield item.entity_id

    # Delete item
    item.delete()


@pytest.fixture(scope="function")
def property_id(py_wb):
    """Create a new Wikibase property (of type string) and delete it after running the test

    :param py_wb: API wrapper class
    :type py_wb: PyWikibase
    :return: Yield the property's ID
    :rtype: str
    """
    # Create property
    prop = py_wb.Property().create(SAMPLE_PROPERTY_LABEL, "string")
    assert prop.entity_id.startswith("P")
    assert prop.label.get(LANGUAGE) == SAMPLE_PROPERTY_LABEL

    # Pass entity_id to test function and wait for it to finish
    yield prop.entity_id

    # Delete property
    prop.delete()
