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

    def visit_UnaryOperation(self, node):

        value = self.visit(node.operand)

        if node.operator == "-":
            return -value

        if node.operator == "+":
            return +value

        if node.operator == "!":
            return not bool(value)

        raise RuntimeError(
            f"Unknown unary operator {node.operator}"
        )
    
    def visit_Block(self, node):

        for statement in node.statements:
            self.visit(statement)

    def visit_IfStatement(self, node):

        condition = self.visit(node.condition)

        if condition:

            self.visit(node.then_block)

        elif node.else_block is not None:

            self.visit(node.else_block)

    def visit_BinaryOperation(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        # Arithmetic
        if node.operator == "+":
            return left + right

        if node.operator == "-":
            return left - right

        if node.operator == "*":
            return left * right

        if node.operator == "/":
            return left / right

        # Comparison
        if node.operator == "==":
            return left == right

        if node.operator == "!=":
            return left != right

        if node.operator == ">":
            return left > right

        if node.operator == "<":
            return left < right

        if node.operator == ">=":
            return left >= right

        if node.operator == "<=":
            return left <= right

        # Logical
        if node.operator == "&&":
            return bool(left) and bool(right)

        if node.operator == "||":
            return bool(left) or bool(right)

        raise RuntimeError(f"Unknown operator {node.operator}")

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
    def visit_String(self, node):

        return node.value


    def visit_Float(self, node):

        return node.value


    def visit_Boolean(self, node):

        return node.value


    def visit_Null(self, node):

        return None