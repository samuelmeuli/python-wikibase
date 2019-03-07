from python_wikibase.base import Base


class Value(Base):
    def __init__(self, py_wb, wb, language):
        super().__init__(py_wb, wb, language)
