from wikibase_api import Wikibase as WikibaseApi

from .data_model.entity import Item, Property

DEFAULT_CONFIG = {
    "api_url": "https://www.wikidata.org/w/api.php",
    "oauth_credentials": None,
    "login_credentials": None,
    "is_bot": False,
    "summary": "Modified using wikibase-api for Python",
}


class Wikibase:
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
        wb = WikibaseApi(
            api_url=api_url,
            oauth_credentials=oauth_credentials,
            login_credentials=login_credentials,
            is_bot=is_bot,
            summary=summary,
            config_path=config_path,
        )

        # Components
        self.item = Item(wb, language)
        self.property = Property(wb, language)
