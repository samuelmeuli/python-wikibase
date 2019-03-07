from wikibase_api import Wikibase as WikibaseApi

from python_wikibase.data_model import (
    Aliases,
    Claim,
    Claims,
    Description,
    Item,
    Label,
    Property,
    Qualifier,
    Qualifiers,
    Reference,
    References,
)
from python_wikibase.data_types import ExternalId, GeoLocation, Quantity, StringValue

DEFAULT_CONFIG = {
    "api_url": "https://www.wikidata.org/w/api.php",
    "oauth_credentials": {},
    "login_credentials": {},
    "is_bot": False,
    "summary": "Modified using wikibase-api for Python",
}


class PyWikibase:
    def __init__(
        self,
        # wikibase-api params
        api_url=DEFAULT_CONFIG["api_url"],
        oauth_credentials=DEFAULT_CONFIG["oauth_credentials"],
        login_credentials=DEFAULT_CONFIG["login_credentials"],
        is_bot=DEFAULT_CONFIG["is_bot"],
        summary=DEFAULT_CONFIG["summary"],
        config_path=None,
        # Other params
        language="en",
    ):
        # Create instance of wikibase-api's Wikibase class (includes authentication)
        self.api = WikibaseApi(
            api_url=api_url,
            oauth_credentials=oauth_credentials,
            login_credentials=login_credentials,
            is_bot=is_bot,
            summary=summary,
            config_path=config_path,
        )
        self.language = language

    # Data model

    def Aliases(self):
        return Aliases(self, self.api, self.language)

    def Claim(self):
        return Claim(self, self.api, self.language)

    def Claims(self):
        return Claims(self, self.api, self.language)

    def Description(self):
        return Description(self, self.api, self.language)

    def Item(self):
        return Item(self, self.api, self.language)

    def Label(self):
        return Label(self, self.api, self.language)

    def Property(self):
        return Property(self, self.api, self.language)

    def Qualifier(self):
        return Qualifier(self, self.api, self.language)

    def Qualifiers(self):
        return Qualifiers(self, self.api, self.language)

    def Reference(self):
        return Reference(self, self.api, self.language)

    def References(self):
        return References(self, self.api, self.language)

    # Data types

    def ExternalId(self):
        return ExternalId(self, self.api, self.language)

    def GeoLocation(self):
        return GeoLocation(self, self.api, self.language)

    def Quantity(self):
        return Quantity(self, self.api, self.language)

    def StringValue(self):
        return StringValue(self, self.api, self.language)
