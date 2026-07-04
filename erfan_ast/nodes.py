from dataclasses import dataclass


class ASTNode:
    pass


# ------------------------
# Program
# ------------------------

@dataclass
class Program(ASTNode):
    statements: list


# ------------------------
# Literals
# ------------------------

@dataclass
class Number(ASTNode):
    value: int


@dataclass
class Float(ASTNode):
    value: float


@dataclass
class String(ASTNode):
    value: str


@dataclass
class Boolean(ASTNode):
    value: bool


@dataclass
class Null(ASTNode):
    pass


# ------------------------
# Identifier
# ------------------------

@dataclass
class Identifier(ASTNode):
    name: str


# ------------------------
# Assignment
# ------------------------

@dataclass
class Assignment(ASTNode):
    target: Identifier
    value: ASTNode


# ------------------------
# Binary Operation
# ------------------------

@dataclass
class BinaryOperation(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOperation(ASTNode):

    operator: str
    operand: ASTNode

# ------------------------
# Function Call
# ------------------------

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: list