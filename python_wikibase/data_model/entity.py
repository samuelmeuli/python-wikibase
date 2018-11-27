from abc import ABC

from ..utils.exceptions import NotFoundError, UpdateError


class Entity(ABC):
    def __init__(self, wb, language, entity_type):
        """Wikibase entity (item or property)

        :param wb: Wikibase API wrapper object
        :type wb: Wikibase
        :param language: Language for searches and edits on Wikibase
        :type language: str
        :param entity_type: One of ["item", "property"]
        :type entity_type: str
        """
        self.wb = wb
        self.language = language
        self.entity_type = entity_type

    def create(self, label, content):
        """Create a new entity with the specified label and content

        :param label: Label of the new entity
        :type label: str
        :param content: Content of the new entity
        :type content: dict
        :return: self
        :rtype: Entity
        """
        r = self.wb.entity.add(self.entity_type, content)
        self.entity_id = r["entity"]["id"]
        self.label = label
        # TODO save (empty) attributes
        return self

    def get(self, entity_id):
        """Fetch information about the specified entity from Wikibase

        :param entity_id: ID of the entity on Wikibase (e.g. "Q1")
        :type entity_id: str
        :return: self
        :rtype: Entity
        """
        r = self.wb.entity.get(entity_id)
        if "success" not in r or r["success"] != 1:
            raise NotFoundError(
                'No {} found with the entity_id "{}"'.format(self.entity_type, self.entity_id)
            )

        entity = r["entities"][entity_id]
        self.entity_id = entity["id"]
        self.label = entity["labels"][self.language]["value"]
        # TODO save attributes
        return self

    def search(self, label):
        """Search Wikibase for entities with the specified label

        :param label: Label of the desired entity
        :type label: str
        :return: List of search results (with entity_id and label)
        :rtype: list
        """
        r = self.wb.entity.search(label, self.language, entity_type=self.entity_type)
        results = r["search"]
        return [{"entity_id": result["id"], "label": result["label"]} for result in results]

    def delete(self):
        """Delete the entity from Wikibase"""
        if self.entity_type == "item":
            title = "Item:" + self.entity_id
        else:
            title = "Property:" + self.entity_id
        self.wb.entity.remove(title)
    def set_label(self, label):
        """Update the entity's label (title)

        :param label: New label
        :type label: str
        """
        r = self.wb.label.set(self.entity_id, label, self.language)
        if (
            "success" not in r
            or "error" in r
            or r["entity"]["labels"][self.language]["value"] != label
        ):
            raise UpdateError("Could not update label: " + r)
        self.label = r["entity"]["labels"][self.language]["value"]



class Item(Entity):
    def __init__(self, wb, language):
        super().__init__(wb, language, "item")

    def create(self, label):
        content = {"labels": {self.language: {"language": self.language, "value": label}}}
        return super().create(label, content)


class Property(Entity):
    def __init__(self, wb, language):
        super().__init__(wb, language, "property")

    def create(self, label, property_type):
        # TODO improve property type handling
        content = {
            "labels": {self.language: {"language": self.language, "value": label}},
            "datatype": property_type,
        }
        return super().create(label, content)
