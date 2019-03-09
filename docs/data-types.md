# Data Types

**Note:** Not all of Wikibase's data types are implemented yet. Trying to parse an item with a value of such a data type will raise a `NotImplementedError`.

## StringValue

Adding a `StringValue` claim to an item:

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")

value = py_wb.StringValue().create("This is a string")

claim = item.claims.add(prop, value)
```

## ExternalId

Adding an `ExternalId` claim to an item:

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")

value = py_wb.ExternalId().create("ID123")

claim = item.claims.add(prop, value)
```

## GeoLocation

Adding a `GeoLocation` claim to an item:

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")

value = py_wb.GeoLocation().create(1.23, 4.56)

claim = item.claims.add(prop, value)
```

Optional parameters:

- `altitude` (`float`, default: `None`)
- `precision` (`float`, default: `1 / 3600`)
- `globe` (`Item`, default: `None`)

## Quantity

Adding a `Quantity` claim to an item:

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")

value = py_wb.Quantity().create(123)

claim = item.claims.add(prop, value)
```

Adding a `Quantity` claim with a unit (must be an item):

```py
item = py_wb.Item().get(entity_id="Q1")
item_unit = py_wb.Item().get(entity_id="Q2")
prop = py_wb.Property().get(entity_id="P1")

value = py_wb.Quantity().create(123, unit=item_unit)

claim = item.claims.add(prop, value)
```
