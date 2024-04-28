from _ast import AST
from typing import Iterable


class InvalidTypeError(Exception):
    type: AST

    def __init__(self, node: AST):
        super().__init__(f"Cannot handle : {node.__class__}. Revisit expression!")
        self.type = node


class InvalidNameError(Exception):
    def __init__(self, name: str, names: Iterable[str]):
        super().__init__(f"No known function called {name}, known are: {names}")
        self.name = name
        self.names = names
