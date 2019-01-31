class_to_data_type = {
    "CommonsMedia": "commonsMedia",
    "ExternalId": "external-id",
    "Form": "wikibase-form",
    "GeoLocation": "globe-coordinate",
    "GeoShape": "geo-shape",
    "Item": "wikibase-item",
    "Lexeme": "wikibase-lexeme",
    "Math": "math",
    "Property": "wikibase-property",
    "Quantity": "quantity",
    "Sense": "wikibase-sense",
    "StringValue": "string",
    "Table": "tabular-data",
    "Time": "time",
    "Url": "url",
}

data_type_to_class = {}

# Populate data_type_to_class
for class_name, data_type in class_to_data_type.items():
    data_type_to_class[data_type] = class_name
