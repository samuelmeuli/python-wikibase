from wikibase_api import Wikibase as WikibaseApi

from .data_model import AliasList, Description, Item, Label, Property

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
        api = WikibaseApi(
            api_url=api_url,
            oauth_credentials=oauth_credentials,
            login_credentials=login_credentials,
            is_bot=is_bot,
            summary=summary,
            config_path=config_path,
        )
        language = language

        self.AliasList = AliasList(self, api, language)
        self.Description = Description(self, api, language)
        self.Label = Label(self, api, language)
        self.Item = Item(self, api, language)
        self.Property = Property(self, api, language)
