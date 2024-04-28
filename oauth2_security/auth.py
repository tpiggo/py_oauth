import ast
from _ast import Call, BoolOp, Expr, AST, Name, Module, Constant, expr
from ast import parse, NodeVisitor as _NodeVisitor
from typing import Type, Union, Any
from .errors import InvalidTypeError, InvalidNameError
from .nodes import Node, registry, And, Or


class NodeVisitor(_NodeVisitor):
    __auth_function_names = registry

    @classmethod
    def extract_constant(cls, a: expr) -> str:
        if isinstance(a, Constant):
            if not isinstance(a.value, str):
                raise TypeError("must be string constant!")
            elif not a.value:
                raise ValueError("must not be an empty string")
            return a.value
        raise TypeError(f"Should be constant! Passed in {type(a)}")

    def visit_Call(self, node: Call) -> Node:
        args = tuple(self.extract_constant(a) for a in node.args)
        auth = self.visit(node.func)
        return auth(*args)

    def visit_Name(self, node: Name) -> Type[Node]:
        value = self.__auth_function_names.get(node.id)
        if value:
            return value
        raise InvalidNameError(node.id, self.__auth_function_names.keys())

    def visit_And(self, node: ast.And) -> Type[Node]:
        return And

    def visit_Or(self, node: ast.Or) -> Type[Node]:
        return Or

    def visit_BoolOp(self, node: BoolOp) -> Node:
        t = self.visit(node.op)
        return t([self.visit(i) for i in node.values])

    def visit_Expr(self, node: Expr) -> Node:
        v = self.visit(node.value)
        return v

    def generic_visit(self, node: AST) -> Any:
        raise InvalidTypeError(node)

    def visit_Module(self, node: Module) -> Any:
        modules = [self.visit(v) for v in node.body]
        if len(modules) > 1:
            raise ValueError("Cannot handle multiple expressions in the module")
        module, = modules
        return module

    def visit(self, ast: AST) -> Union[Type[Node], Node]:
        return super().visit(ast)


def pre_authorize_expression(expr: str) -> Node:
    """
    Reads the expression and parses it. Ensures, expression is valid
    :param expr: string expression
    :return: parsed expression as executable tree
    """
    parsed_ast = parse(expr)
    node_visitor = NodeVisitor()
    return node_visitor.visit(parsed_ast)
