# python-wikibase

**`python-wikibase` provides an object-oriented abstraction of the [Wikibase API](https://www.wikidata.org/w/api.php?action=help).**

The library simplifies the authentication process and can be used to query and edit information on Wikidata or any other Wikibase instance.

## Example

```py
from python_wikibase import PyWikibase

# Authenticate with Wikibase
py_wb = PyWikibase(config_path="config.json")

# Fetch item and "coordinate location" property
item = py_wb.Item().get(entity_id="item label")
prop = py_wb.Property().get(entity_id="coordinate location")

# Create new GeoLocation value
value = py_wb.GeoLocation().create(1.23, 4.56)

# Create GeoLocation claim
claim = item.claims.add(prop, value)
```

## Installation

```sh
pip install python-wikibase
```

## Authentication

The `PyWikibase` class takes the same authentication and configuration parameters as the `WikibaseApi` class from the [`wikibase-api`](https://github.com/samuelmeuli/wikibase-api) library. See its documentation for a guide on how to authenticate with Wikibase.

## Usage

→ [Documentation](docs/usage.md)
