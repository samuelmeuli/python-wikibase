# Labels, Aliases and Descriptions

## Label

### Getting an item/property's label

Getting an item's label in the default language:

```py
label = str(item.label)
# or
label = item.label.get()
```

Getting an item's label in Dutch:

```py
label = item.label.get(language="nl")
```

### Updating an item/property's label

Updating an item's label in the default language to "new label":

```py
item.label.set("new label")
```

Updating an item's Spanish label to "nuevo título":

```py
item.label.set("nuevo título", language="es")
```

## Alias

### Getting an item/property's aliases

Getting an item's aliases in the default language:

```py
aliases = list(item.aliases)
# or
aliases = item.aliases.get()
```

Getting an item's aliases in Polish:

```py
aliases = item.aliases.get(language="pl")
```

### Adding an alias

Adding "new alias" to an item's aliases for the default language:

```py
item.aliases.add("new alias")
```

Adding "nouvel alias" to an item's French aliases:

```py
item.aliases.add("nouvel alias", language="fr")
```

### Deleting an alias

Deleting "some alias" from an item's aliases for the default language:

```py
item.aliases.remove("some alias")
```

Deleting "ein Alias" from an item's German aliases:

```py
item.aliases.remove("ein Alias", language="de")
```

## Description

### Getting an item/property's description

Getting an item's description in the default language:

```py
description = str(item.description)
# or
description = item.description.get()
```

Getting an item's description in Portuguese:

```py
description = item.description.get(language="pt")
```

### Updating an item/property's description

Updating an item's description in the default language to "new description":

```py
item.description.set("new description")
```

Updating an item's Swedish description to "ny beskrivning":

```py
item.description.set("ny beskrivning", language="sv")
```
