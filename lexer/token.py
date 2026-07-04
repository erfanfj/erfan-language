from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # Special
    EOF = auto()
    NEWLINE = auto()

    # Literals
    NUMBER = auto()
    IDENTIFIER = auto()

    # Operators
    ASSIGN = auto()      # <-
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /

    # Symbols
    LPAREN = auto()      # (
    RPAREN = auto()      # )

    # Built-in Keywords
    CHAP = auto()


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

    def __repr__(self):
        return (
            f"Token("
            f"{self.type.name}, "
            f"{self.value}, "
            f"line={self.line}, "
            f"column={self.column})"
        )