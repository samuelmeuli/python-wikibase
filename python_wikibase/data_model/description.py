import json

from wikibase_api import ApiError

from python_wikibase.base import Base
from python_wikibase.utils.exceptions import DuplicateError, EditError


class Description(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.descriptions = {}
        self.item_id = None

    def __str__(self):
        return self.get()

    def unmarshal(self, item_id, descriptions):
        self.item_id = item_id
        for lang, lang_value in descriptions.items():
            self.descriptions[lang] = lang_value["value"]
        return self

    def get(self, language=None):
        """Get the entity's description in the specified language (or use the entity's default)

        :param language: Language to get the description for
        :type language: str
        :return: Description
        :rtype: str
        """
        if not language:
            language = self.language
        if language not in self.descriptions:
            return None
        return self.descriptions[language]

    def set(self, description, language=None):
        """Update the entity's description in the specified language (or the entity's default)

        :param description: Description to replace the current one with
        :type description: str
        :param language: Language to update the description for
        :type language: str
        """
        if not language:
            language = self.language

        try:
            r = self.api.description.set(self.item_id, description, language)
            self.descriptions[language] = r["entity"]["descriptions"][language]["value"]
        except ApiError as e:
            r_dict = json.loads(str(e))
            if (
                "messages" in r_dict
                and r_dict["messages"][0]["name"]
                == "wikibase-validator-label-with-description-conflict"
            ):
                raise DuplicateError(
                    "Another entity with the same label and description already exists"
                ) from None
            else:
                raise EditError(f"Could not update description: {e}") from None
