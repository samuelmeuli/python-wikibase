from wikibase_api import ApiError

from ..base import Base
from ..utils.exceptions import EditError


class Label(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.item_id = None
        self.labels = {}

    def unmarshal(self, item_id, labels):
        self.item_id = item_id
        for lang, lang_value in labels.items():
            self.labels[lang] = lang_value["value"]
        return self

    def get(self, language=None):
        """Get the entity's label in the specified language (or use the entity's default)

        :param language: Language to get the label in
        :type language: str
        :return: Label
        :rtype: str
        """
        if not language:
            language = self.language
        return self.labels[language]

    def set(self, new_label, language=None):
        """Update the entity's label in the specified language (or the entity's default)

        :param new_label: New label to use
        :type new_label: str
        :param language: Language to update the label for
        :type language: str
        """
        if not language:
            language = self.language

        try:
            r = self.api.label.set(self.item_id, new_label, language)
            self.labels[language] = r["entity"]["labels"][language]["value"]
        except ApiError as e:
            raise EditError(f"Could not update label: {e}") from None
