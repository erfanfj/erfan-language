from .token import TokenType

KEYWORDS = {
    "chap": TokenType.CHAP,

    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,

    "if": TokenType.IF,
    "else": TokenType.ELSE,

    "fn": TokenType.FN,
    "return": TokenType.RETURN,

    "class": TokenType.CLASS,
    "this": TokenType.THIS,

    "boro": TokenType.BORO,
    "roye": TokenType.ROYE,
    "while": TokenType.WHILE,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
}