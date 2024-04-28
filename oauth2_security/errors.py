from _ast import AST
from typing import Iterable


class InvalidTypeError(Exception):
    """
    Exception for handling invalid type exceptions which are known to be unknown/invalid operations in the AST, such as
    imports, additions, etc.
    """
    type: AST

    def __init__(self, node: AST):
        super().__init__(f"Cannot handle : {node.__class__}. Revisit expression!")
        self.type = node


class InvalidNameError(Exception):
    """
    Exception for handling invalid name exceptions which are known to be unknown names registered to the flyway
    """

    def __init__(self, name: str, names: Iterable[str]):
        super().__init__(f"No known function called {name}, known are: {names}")
        self.name = name
        self.names = names
