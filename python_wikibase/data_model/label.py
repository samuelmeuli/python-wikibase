import json

from wikibase_api import ApiError

from python_wikibase.base import Base
from python_wikibase.utils.exceptions import DuplicateError, EditError


class Label(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.item_id = None
        self.labels = {}

    def __str__(self):
        return self.get()

    def unmarshal(self, item_id, labels):
        self.item_id = item_id
        for lang, lang_value in labels.items():
            self.labels[lang] = lang_value["value"]
        return self

    def get(self, language=None):
        """Get the entity's label in the specified language (or use the entity's default)

        :param language: Language to get the label for
        :type language: str
        :return: Label
        :rtype: str
        """
        if not language:
            language = self.language
        if language not in self.labels:
            return None
        return self.labels[language]

    def set(self, label, language=None):
        """Update the entity's label in the specified language (or the entity's default)

        :param label: Label to replace the current one with
        :type label: str
        :param language: Language to update the label for
        :type language: str
        """
        if not language:
            language = self.language

        try:
            r = self.api.label.set(self.item_id, label, language)
            self.labels[language] = r["entity"]["labels"][language]["value"]
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
                raise EditError(f"Could not set label: {e}") from None
