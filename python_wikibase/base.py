from abc import ABC


class Base(ABC):
    def __init__(self, py_wb, api, language):
        self.py_wb = py_wb
        self.api = api
        self.language = language
