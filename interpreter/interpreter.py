from erfan_ast.nodes import (
    Program,
    Assignment,
    Identifier,
    Number,
    BinaryOperation,
    FunctionCall,
)

from interpreter.environment import Environment
from interpreter.builtin import Builtins


class Interpreter:

    def __init__(self):

        self.env = Environment()

    # ----------------------------------------

    def visit(self, node):

        method = getattr(
            self,
            f"visit_{type(node).__name__}"
        )

        return method(node)

    # ----------------------------------------

    def visit_Program(self, node):

        for statement in node.statements:
            self.visit(statement)

    # ----------------------------------------

    def visit_Number(self, node):

        return node.value

    # ----------------------------------------

    def visit_Identifier(self, node):

        return self.env.get(node.name)

    # ----------------------------------------

    def visit_Assignment(self, node):

        value = self.visit(node.value)

        self.env.set(
            node.target.name,
            value
        )

    # ----------------------------------------

    def visit_BinaryOperation(self, node):

        left = self.visit(node.left)

        right = self.visit(node.right)

        if node.operator == "+":
            return left + right

        if node.operator == "-":
            return left - right

        if node.operator == "*":
            return left * right

        if node.operator == "/":
            return left / right

        raise Exception("Unknown operator")

    # ----------------------------------------

    def visit_FunctionCall(self, node):

        args = [
            self.visit(arg)
            for arg in node.arguments
        ]

        if node.name == "chap":
            Builtins.chap(*args)
            return

        raise Exception(
            f"Unknown function '{node.name}'"
        )