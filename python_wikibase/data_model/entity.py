from ..base import Base
from ..utils.exceptions import EditError, NotFoundError
from ..utils.property_types import property_types


class Entity(Base):
    def __init__(self, py_wb, api, language, entity_type):
        """Wikibase entity (item or property)

        :param wb: Wikibase API wrapper object
        :type wb: Wikibase
        :param language: Language for searches and edits on Wikibase
        :type language: str
        :param entity_type: One of ["item", "property"]
        :type entity_type: str
        """
        self.entity_type = entity_type
        self.entity_id = None
        self.label = None
        self.description = None
        self.aliases = None

        super().__init__(py_wb, api, language)

    def _create(self, label, content):
        """Create a new entity with the specified label and content

        :param label: Label of the new entity
        :type label: str
        :param content: Content of the new entity
        :type content: dict
        :return: self
        :rtype: Entity
        """
        # Create entity
        r = self.api.entity.add(self.entity_type, content)
        entity = r["entity"]

        # Save entity_id and label
        self.entity_id = entity["id"]
        self.label = self.py_wb.Label().unmarshal(self.entity_id, entity["labels"])

        # Save empty attributes
        self.description = self.py_wb.Description().unmarshal(self.entity_id, {})
        self.aliases = self.py_wb.AliasList().unmarshal(self.entity_id, {})

        return self

    def get(self, entity_id):
        """Fetch information about the specified entity from Wikibase

        :param entity_id: ID of the entity on Wikibase (e.g. "Q1")
        :type entity_id: str
        :return: self
        :rtype: Entity
        """
        r = self.api.entity.get(entity_id)
        if "success" not in r or r["success"] != 1:
            raise NotFoundError(
                'No {} found with the entity_id "{}"'.format(self.entity_type, self.entity_id)
            )

        entity = r["entities"][entity_id]
        if "missing" in entity:
            raise NotFoundError(
                'No {} found with the entity_id "{}"'.format(self.entity_type, self.entity_id)
            )

        # Save entity_id and label
        self.entity_id = entity["id"]
        # Descriptions
        self.label = self.py_wb.Label().unmarshal(self.entity_id, entity["labels"])

        # Save other attributes
        self.description = self.py_wb.Description().unmarshal(
            self.entity_id, entity["descriptions"]
        )
        self.aliases = self.py_wb.AliasList().unmarshal(self.entity_id, entity["aliases"])

        return self

    def search(self, label):
        """Search Wikibase for entities with the specified label

        :param label: Label of the desired entity
        :type label: str
        :return: List of search results (with entity_id and label)
        :rtype: list
        """
        r = self.api.entity.search(label, self.language, entity_type=self.entity_type)
        results = r["search"]
        return [{"entity_id": result["id"], "label": result["label"]} for result in results]

    def delete(self):
        """Delete the entity from Wikibase"""
        if self.entity_type == "item":
            title = "Item:" + self.entity_id
        else:
            title = "Property:" + self.entity_id
        r = self.api.entity.remove(title)
        if "delete" not in r or "error" in r:
            raise EditError("Could not delete entity: " + r)


class Item(Entity):
    def __init__(self, py_wb, wb, language):
        super().__init__(py_wb, wb, language, "item")

    def create(self, label):
        content = {"labels": {self.language: {"language": self.language, "value": label}}}
        return super()._create(label, content)


class Property(Entity):
    def __init__(self, py_wb, wb, language):
        super().__init__(py_wb, wb, language, "property")

    def create(self, label, property_type="string"):
        if property_type not in property_types:
            raise ValueError(
                f'"{property_type}" is not a valid property_type, must be one of must be one of '
                "{property_types}"
            )
        content = {
            "labels": {self.language: {"language": self.language, "value": label}},
            "datatype": property_type,
        }
        return super()._create(label, content)
