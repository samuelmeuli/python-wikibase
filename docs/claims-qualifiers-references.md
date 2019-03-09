# Claims, Qualifiers and References

## Claims

### Getting claims

Getting an item/property's claims as a list:

```py
item = py_wb.Item().get(entity_id="Q1")
claim_list = list(item.claims)
# or
claim_list = item.claims.to_list()
# Returns list of the following form:
# [<Claim>, <Claim>, <Claim>]
```

Getting an item/property's claims as a dict:

```py
item = py_wb.Item().get(entity_id="Q1")
claim_list = item.claims.to_dict()
# Returns dict of the following form:
# {
#     "P1": [<Claim>],
#     "P2": [<Claim>, <Claim>]
# }
```

### Adding a claim

Adding a claim of property "P1" with a **string value** to the item "Q1" (works the same way for all data types):

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")
value = py_wb.StringValue().create("This is a string")
item.claims.add(prop, value)
```

Adding a claim of property "P1" with **no value** to the item "Q1":

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")
item.claims.add_no_value(prop)
```

Adding a claim of property "P1" with an **unknown value** to the item "Q1":

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")
item.claims.add_some_value(prop)
```

### Updating a claim

Updating a claim's **string value** (works the same way for all data types):

```py
value = py_wb.StringValue().create("This is a string")
claim.set_value(value)
```

Updating a claim to have **no value**:

```py
claim.set_no_value()
```

Updating a claim to have an **unknown value**:

```py
claim.set_some_value()
```

### Deleting a claim

Deleting a claim from an item:

```py
item = py_wb.Item().get(entity_id="Q1")
claim = item.claims[0]
item.claims.remove(claim)
```

## Qualifiers

`claim.qualifiers` supports the same functions as `item.claims` (see above).

For example, you can add a qualifier with a string value to a claim:

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")
claim = item.claims[0]
value = py_wb.StringValue().create("This is a string")
claim.qualifiers.add(prop, value)
```

## References

`claim.references` supports the same functions as `item.claims` (see above).

For example, you can add a reference with a string value to a claim:

```py
item = py_wb.Item().get(entity_id="Q1")
prop = py_wb.Property().get(entity_id="P1")
claim = item.claims[0]
value = py_wb.StringValue().create("This is a string")
claim.references.add(prop, value)
```
