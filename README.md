# python-wikibase

**`python-wikibase` provides an object-oriented abstraction of the [Wikibase API](https://www.wikidata.org/w/api.php?action=help).**

The library simplifies the authentication process and can be used to query and edit information on Wikidata or any other Wikibase instance.

## Installation

```sh
pip install python-wikibase
```

## Usage

Simple example for adding a coordinate location claim to an existing Wikibase item:

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

**See the [documentation](./docs/usage.md) for descriptions and examples of all commands.**

## Authentication

The `PyWikibase` class takes the same authentication and configuration parameters as the `WikibaseApi` class from the [`wikibase-api`](https://github.com/samuelmeuli/wikibase-api) library (which is used internally). See [its documentation](https://wikibase-api.readthedocs.io/en/latest/getting_started/installation_and_usage.html#edits) for a guide on how to authenticate with Wikibase.

## Development

### Setup

See [this guide](https://wikibase-api.readthedocs.io/en/latest/development/development.html) on how to set up a development environment for this package.

If you'd like to test this package with a local instance of Wikibase, see [this guide](https://wikibase-api.readthedocs.io/en/latest/guides/local_wikibase_instance.html) on how to set up a development instance with `wikibase-docker`.

### Contributing

Suggestions and contributions are always welcome! Please first discuss changes via issue before submitting a pull request.
