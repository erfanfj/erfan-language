from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):

    # --------------------------
    # Special
    # --------------------------

    EOF = auto()
    NEWLINE = auto()

    # --------------------------
    # Literals
    # --------------------------

    # Keywords
    IF = auto()
    ELSE = auto()
    FN = auto()
    RETURN = auto()
    CLASS = auto()
    THIS = auto()

    # Symbols
    LBRACE = auto()   # {
    RBRACE = auto()   # }

    NUMBER = auto()
    FLOAT = auto()
    STRING = auto()

    IDENTIFIER = auto()

    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    # --------------------------
    # Operators
    # --------------------------

    ASSIGN = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    # --------------------------
    # Comparison
    # --------------------------

    EQ = auto()
    NE = auto()

    GT = auto()
    LT = auto()

    GTE = auto()
    LTE = auto()

    # --------------------------
    # Logic
    # --------------------------

    AND = auto()
    OR = auto()
    NOT = auto()

    # --------------------------
    # Symbols
    # --------------------------

    LPAREN = auto()
    RPAREN = auto()

    COMMA = auto()
    DOT = auto()

    # --------------------------
    # Builtin
    # --------------------------

    CHAP = auto()


@dataclass
class Token:

    type: TokenType
    value: object

    line: int
    column: int

    def __repr__(self):

        return f"Token({self.type.name}, {self.value}, line={self.line}, column={self.column})"