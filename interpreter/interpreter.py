from erfan_ast.nodes import (
    Program,
    Assignment,
    Identifier,
    MemberAccess,
    IndexAccess,
)

from interpreter.environment import Environment
from interpreter.builtin import Builtins
from interpreter.objects import ErfanInstance


class ReturnException(Exception):

    def __init__(self, value):
        self.value = value


class BreakException(Exception):
    pass


class ContinueException(Exception):
    pass


class Interpreter:

    def __init__(self):

        self.env = Environment()
        self.functions = {}
        self.classes = {}
        self.current_this = None

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

    def visit_This(self, node):

        if self.current_this is None:
            raise RuntimeError("'this' can only be used inside a method")

        return self.current_this

    # ----------------------------------------

    def visit_ArrayLiteral(self, node):

        return [
            self.visit(element)
            for element in node.elements
        ]

    def visit_IndexAccess(self, node):

        obj = self.visit(node.object)
        index = self.visit(node.index)

        if not isinstance(index, int):
            raise TypeError("Array index must be an integer")

        if isinstance(obj, list):
            if index < 0 or index >= len(obj):
                raise IndexError(f"Array index {index} out of range")
            return obj[index]

        if isinstance(obj, str):
            if index < 0 or index >= len(obj):
                raise IndexError(f"String index {index} out of range")
            return obj[index]

        raise TypeError("Index access requires an array or string")

    def set_index(self, target, value):

        obj = self.visit(target.object)
        index = self.visit(target.index)

        if not isinstance(index, int):
            raise TypeError("Array index must be an integer")

        if isinstance(obj, list):
            if index < 0 or index >= len(obj):
                raise IndexError(f"Array index {index} out of range")
            obj[index] = value
            return

        raise TypeError("Index assignment requires an array")

    # ----------------------------------------

    def visit_Assignment(self, node):

        value = self.visit(node.value)

        if isinstance(node.target, Identifier):
            self.env.set(node.target.name, value)
            return

        if isinstance(node.target, MemberAccess):
            obj = self.visit(node.target.object)

            if not isinstance(obj, ErfanInstance):
                raise RuntimeError("Cannot assign to a member of a non-object value")

            obj.fields[node.target.member] = value
            return

        if isinstance(node.target, IndexAccess):
            self.set_index(node.target, value)
            return

        raise RuntimeError("Invalid assignment target")

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

    def visit_ForInStatement(self, node):

        iterable = self.visit(node.iterable)

        if not isinstance(iterable, (list, str)):
            raise TypeError("for-in loop requires an array or string")

        for item in iterable:
            self.env.set(node.variable, item)

            try:
                self.visit(node.body)
            except ContinueException:
                continue
            except BreakException:
                break

    def visit_WhileStatement(self, node):

        while self.visit(node.condition):
            try:
                self.visit(node.body)
            except ContinueException:
                continue
            except BreakException:
                break

    def visit_BreakStatement(self, node):

        raise BreakException()

    def visit_ContinueStatement(self, node):

        raise ContinueException()

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

        if node.operator == "%":
            return left % right

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

        if node.operator == "&&":
            return bool(left) and bool(right)

        if node.operator == "||":
            return bool(left) or bool(right)

        raise RuntimeError(f"Unknown operator {node.operator}")

    # ----------------------------------------

    def visit_ClassDef(self, node):

        self.classes[node.name] = node

    def visit_FunctionDef(self, node):

        self.functions[node.name] = node

    def visit_ReturnStatement(self, node):

        value = self.visit(node.value)

        raise ReturnException(value)

    def get_method(self, class_def, name):

        for method in class_def.methods:
            if method.name == name:
                return method

        return None

    def call_function(self, func, args):

        if len(args) != len(func.params):
            raise RuntimeError(
                f"Function '{func.name}' expected {len(func.params)} "
                f"arguments but got {len(args)}"
            )

        previous_env = self.env
        previous_this = self.current_this

        self.env = Environment(parent=previous_env)
        self.current_this = None

        for param, arg in zip(func.params, args):
            self.env.set(param, arg)

        try:
            self.visit(func.body)
            result = None
        except ReturnException as exc:
            result = exc.value
        finally:
            self.env = previous_env
            self.current_this = previous_this

        return result

    def call_method(self, instance, method_name, args):

        method = self.get_method(instance.class_def, method_name)

        if method is None:
            raise RuntimeError(
                f"Class '{instance.class_def.name}' has no method '{method_name}'"
            )

        if len(args) != len(method.params):
            raise RuntimeError(
                f"Method '{method_name}' expected {len(method.params)} "
                f"arguments but got {len(args)}"
            )

        previous_env = self.env
        previous_this = self.current_this

        self.env = Environment(parent=previous_env)
        self.current_this = instance

        for param, arg in zip(method.params, args):
            self.env.set(param, arg)

        try:
            self.visit(method.body)
            result = None
        except ReturnException as exc:
            result = exc.value
        finally:
            self.env = previous_env
            self.current_this = previous_this

        return result

    def instantiate(self, class_def, args):

        init = self.get_method(class_def, "init")

        if init is None and args:
            raise RuntimeError(
                f"Class '{class_def.name}' has no init method but received arguments"
            )

        instance = ErfanInstance(class_def)

        if init is not None:
            self.call_method(instance, "init", args)

        return instance

    def visit_MemberAccess(self, node):

        obj = self.visit(node.object)

        if not isinstance(obj, ErfanInstance):
            raise RuntimeError("Member access requires an object")

        if node.member not in obj.fields:
            raise AttributeError(
                f"'{obj.class_def.name}' object has no attribute '{node.member}'"
            )

        return obj.fields[node.member]

    def visit_MethodCall(self, node):

        obj = self.visit(node.object)

        if not isinstance(obj, ErfanInstance):
            raise RuntimeError("Method calls require an object")

        args = [
            self.visit(arg)
            for arg in node.arguments
        ]

        return self.call_method(obj, node.method, args)

    def visit_FunctionCall(self, node):

        args = [
            self.visit(arg)
            for arg in node.arguments
        ]

        if node.name == "chap":
            Builtins.chap(*args)
            return None

        if node.name == "size":
            if len(args) != 1:
                raise RuntimeError("size() expects exactly 1 argument")
            return Builtins.size(args[0])

        if node.name in self.classes:
            return self.instantiate(self.classes[node.name], args)

        if node.name in self.functions:
            return self.call_function(self.functions[node.name], args)

        raise Exception(
            f"Unknown function or class '{node.name}'"
        )

    def visit_String(self, node):

        return node.value

    def visit_Float(self, node):

        return node.value

    def visit_Boolean(self, node):

        return node.value

    def visit_Null(self, node):

        return None
