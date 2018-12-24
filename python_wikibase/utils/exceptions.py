# Searching


class SearchError(Exception):
    pass


class NotFoundError(SearchError):
    pass


# Editing


class EditError(Exception):
    pass


class DuplicateError(EditError):
    pass
