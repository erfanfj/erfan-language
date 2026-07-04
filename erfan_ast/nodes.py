from dataclasses import dataclass, field
from typing import List, Any


# ==========================================================
# Base Node
# ==========================================================

class ASTNode:
    pass


# ==========================================================
# Program
# ==========================================================

@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)


# ==========================================================
# Literals
# ==========================================================

@dataclass
class Number(ASTNode):
    value: int


@dataclass
class String(ASTNode):
    value: str


@dataclass
class Boolean(ASTNode):
    value: bool


# ==========================================================
# Identifier
# ==========================================================

@dataclass
class Identifier(ASTNode):
    name: str


# ==========================================================
# Expressions
# ==========================================================

@dataclass
class BinaryOperation(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOperation(ASTNode):
    operator: str
    operand: ASTNode


# ==========================================================
# Assignment
# ==========================================================

@dataclass
class Assignment(ASTNode):
    target: Identifier
    value: ASTNode


# ==========================================================
# Function Call
# ==========================================================

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List[ASTNode] = field(default_factory=list)