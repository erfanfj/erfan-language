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
    target: ASTNode
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


@dataclass
class Block(ASTNode):
    statements: list


# -----------------------------
# If Statement
# -----------------------------

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_block: Block
    else_block: Block | None = None


# -----------------------------
# Functions
# -----------------------------

@dataclass
class FunctionDef(ASTNode):
    name: str
    params: list
    body: Block


@dataclass
class ReturnStatement(ASTNode):
    value: ASTNode


# -----------------------------
# Classes / OOP
# -----------------------------

@dataclass
class ClassDef(ASTNode):
    name: str
    methods: list


@dataclass
class This(ASTNode):
    pass


@dataclass
class MemberAccess(ASTNode):
    object: ASTNode
    member: str


@dataclass
class MethodCall(ASTNode):
    object: ASTNode
    method: str
    arguments: list


# -----------------------------
# Loops & Collections
# -----------------------------

@dataclass
class ArrayLiteral(ASTNode):
    elements: list


@dataclass
class IndexAccess(ASTNode):
    object: ASTNode
    index: ASTNode


@dataclass
class ForInStatement(ASTNode):
    variable: str
    iterable: ASTNode
    body: Block


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: Block


@dataclass
class BreakStatement(ASTNode):
    pass


@dataclass
class ContinueStatement(ASTNode):
    pass