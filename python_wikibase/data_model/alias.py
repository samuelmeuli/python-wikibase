from wikibase_api import ApiError

from python_wikibase.base import Base
from python_wikibase.utils.exceptions import EditError


class Aliases(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.aliases = {}
        self.item_id = None

    def __getitem__(self, index):
        return self.get()[index]

    def __iter__(self):
        return iter(self.get())

    def __len__(self):
        return len(self.get())

    def unmarshal(self, item_id, aliases):
        self.item_id = item_id
        for lang, alias_list in aliases.items():
            self.aliases[lang] = [alias_item["value"] for alias_item in alias_list]
        return self

    def get(self, language=None):
        """Get the entity's aliases in the specified language (or use the entity's default)

        :param language: Language to get the aliases for
        :type language: str
        :return: Aliases
        :rtype: list(str)
        """
        if not language:
            language = self.language
        if language not in self.aliases:
            return []
        return self.aliases[language]

    def add(self, alias, language=None):
        """Add a new alias in the specified language (or the entity's default)

        :param alias: Alias to add
        :type alias: str
        :param language: Language of the alias to add
        :type language: str
        """
        if not language:
            language = self.language

        try:
            r = self.api.alias.add(self.item_id, alias, language)
            aliases = r["entity"]["aliases"]
            for lang, alias_list in aliases.items():
                self.aliases[lang] = [alias_item["value"] for alias_item in alias_list]
        except ApiError as e:
            raise EditError(f"Could not add alias: {e}") from None

    def remove(self, alias, language=None):
        """Remove the provided alias in the specified language (or the entity's default)

        :param alias: Alias to remove
        :type alias: str
        :param language: Language of the alias to remove
        :type language: str
        """
        if not language:
            language = self.language

        try:
            self.api.alias.remove(self.item_id, alias, language)
            self.aliases[language].remove(alias)
        except ApiError as e:
            raise EditError(f"Could not remove alias: {e}") from None
