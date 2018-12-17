from ..base import Base
from ..utils.exceptions import EditError


class AliasList(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.aliases = {}
        self.entity_id = None

    def unmarshal(self, entity_id, aliases):
        self.entity_id = entity_id
        for lang, alias_list in aliases.items():
            self.aliases[lang] = [alias_item["value"] for alias_item in alias_list]
        return self

    def get(self, language=None):
        """Get the entity's aliases in the specified language (or use the entity's default)

        :param language: Language to get the aliases in
        :type language: str
        :return: Aliases
        :rtype: list(str)
        """
        if not language:
            language = self.language
        return self.aliases[language]

    def add(self, alias, language=None):
        """Add a new alias in the specified language (or the entity's default)

        :param alias: New alias
        :type alias: str
        :param language: Language of the alias to add
        :type language: str
        """
        if not language:
            language = self.language

        r = self.api.alias.add(self.entity_id, alias, language)
        if "success" not in r or "error" in r:
            raise EditError(f"Could not add alias: {r}")
        aliases = r["entity"]["aliases"]
        for lang, alias_list in aliases.items():
            self.aliases[lang] = [alias_item["value"] for alias_item in alias_list]

    def remove(self, alias, language=None):
        """Remove the provided alias in the specified language (or the entity's default)

        :param alias: Alias to remove
        :type alias: str
        :param language: Language of the alias to remove
        :type language: str
        """
        if not language:
            language = self.language

        r = self.api.alias.remove(self.entity_id, alias, language)
        if "success" not in r or "error" in r:
            raise EditError(f"Could not remove alias: {r}")
        self.aliases[language].remove(alias)
