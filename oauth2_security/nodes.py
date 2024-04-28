import dataclasses
import inspect
from abc import ABC
from typing import Type, Union

from .token_info import TokenInfo


class Node:
    def evaluate(self, v: TokenInfo):
        raise NotImplementedError("")


class Mappable:
    @property
    def __function_name__(self) -> str:
        raise NotImplementedError("Requires implementation")


"""
Flyway registry for handling node types (only terminal types in the tree are named nodes)
"""
registry: dict[str, Type[Node]] = {}


def validate_register(cls: Union[callable, Type["Mappable"]]):
    if inspect.isfunction(cls):
        return validate_register(cls())
    if not cls.__function_name__:
        raise ValueError("No function name associated to this type")
    registry[cls.__function_name__] = cls
    return cls


@validate_register
@dataclasses.dataclass
class Authority(Node, Mappable):
    value: str
    __function_name__ = 'has_authority'

    def evaluate(self, v):
        return self.value in v.granted_authorities


@validate_register
@dataclasses.dataclass
class Role(Node, Mappable):
    value: str
    __function_name__ = 'has_role'

    def evaluate(self, v):
        return self.value in v.granted_roles


@validate_register
class AnyRole(Node, Mappable):
    values: tuple[str]
    __function_name__ = 'has_any_role'

    def __init__(self, *args: str):
        self.values = args

    def evaluate(self, v: TokenInfo):
        return any(filter(lambda x: x in self.values, v.granted_roles))


@dataclasses.dataclass
class Expression(ABC, Node):
    items: list[Node]


class Or(Expression):
    def evaluate(self, v):
        for i in self.items:
            if i.evaluate(v):
                return True
        return False


class And(Expression):
    def evaluate(self, v):
        for i in self.items:
            if not i.evaluate(v):
                return False
        return True
