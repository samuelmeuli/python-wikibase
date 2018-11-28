from ..utils.exceptions import EditError


class Description:
    def __init__(self, entity, descriptions):
        self.entity = entity

        self.descriptions = {}
        for lang, lang_value in descriptions.items():
            self.descriptions[lang] = lang_value["value"]

    def __repr__(self):
        return repr(self.descriptions)

    def get(self, language=None):
        """Get the entity's description in the specified language (or use the entity's default)

        :param language: Language to get the description in
        :type language: str
        :return: Description
        :rtype: str
        """
        if not language:
            language = self.entity.language

        return self.descriptions[language]

    def set(self, new_description, language=None):
        """Update the entity's description in the specified language (or the entity's default)

        :param language: Language to update the description for
        :type language: str
        """
        if not language:
            language = self.entity.language

        r = self.entity.wb.description.set(self.entity.entity_id, new_description, language)
        if (
            "success" not in r
            or "error" in r
            or r["entity"]["descriptions"][language]["value"] != new_description
        ):
            raise EditError("Could not update description: " + r)
        self.descriptions[language] = r["entity"]["descriptions"][language]["value"]
