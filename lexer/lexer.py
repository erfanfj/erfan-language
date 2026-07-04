from .token import Token, TokenType
from .keywords import KEYWORDS


SINGLE_CHAR_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,

    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,

    ">": TokenType.GT,
    "<": TokenType.LT,

    "!": TokenType.NOT,   
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
}

DOUBLE_CHAR_TOKENS = {
    "<-": TokenType.ASSIGN,

    "==": TokenType.EQ,
    "!=": TokenType.NE,
    ">=": TokenType.GTE,
    "<=": TokenType.LTE,

    "&&": TokenType.AND,
    "||": TokenType.OR,
}

class Lexer:

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

        self.line = 1
        self.column = 1

        self.current_char = self.text[0] if self.text else None

    def advance(self):

        if self.current_char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.pos += 1

        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    def string(self):

        start = self.column

        self.advance()

        value = ""

        while self.current_char is not None and self.current_char != '"':

            value += self.current_char

            self.advance()

        if self.current_char != '"':

            raise SyntaxError(
                f"Unterminated string at line {self.line}"
            )

        self.advance()

        return Token(
            TokenType.STRING,
            value,
            self.line,
            start
        )

    def peek(self):

        if self.pos + 1 >= len(self.text):
            return None

        return self.text[self.pos + 1]

    def skip_whitespace(self):

        while self.current_char is not None and self.current_char in " \t\r":
            self.advance()

    def number(self):

        start = self.column

        value = ""

        dot = False

        while self.current_char is not None:

            if self.current_char.isdigit():

                value += self.current_char

                self.advance()

                continue

            if self.current_char == ".":

                if dot:

                    break

                dot = True

                value += "."

                self.advance()

                continue

            break

        if dot:

            return Token(
                TokenType.FLOAT,
                float(value),
                self.line,
                start
            )

        return Token(
            TokenType.NUMBER,
            int(value),
            self.line,
            start
        )
    
    def skip_comment(self):

        while self.current_char is not None and self.current_char != "\n":

            self.advance()

    def identifier(self):

        start = self.column
        value = ""

        while (
            self.current_char is not None
            and (
                self.current_char.isalnum()
                or self.current_char == "_"
            )
        ):
            value += self.current_char
            self.advance()

        token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)

        return Token(
            token_type,
            value,
            self.line,
            start
        )

    def tokenize(self):

        tokens = []

        while self.current_char is not None:

            # ---------------------------------------
            # Whitespace
            # ---------------------------------------

            if self.current_char in " \t\r":
                self.skip_whitespace()
                continue

            # ---------------------------------------
            # New Line
            # ---------------------------------------

            if self.current_char == "\n":

                tokens.append(
                    Token(
                        TokenType.NEWLINE,
                        "\\n",
                        self.line,
                        self.column
                    )
                )

                self.advance()
                continue

            # ---------------------------------------
            # Comments
            # ---------------------------------------

            if self.current_char == "/" and self.peek() == "/":

                self.skip_comment()
                continue

            # ---------------------------------------
            # Numbers
            # ---------------------------------------

            if self.current_char.isdigit():

                tokens.append(self.number())
                continue

            # ---------------------------------------
            # String
            # ---------------------------------------

            if self.current_char == '"':

                tokens.append(self.string())
                continue

            # ---------------------------------------
            # Identifier / Keyword
            # ---------------------------------------

            if self.current_char.isalpha() or self.current_char == "_":

                tokens.append(self.identifier())
                continue

            # ---------------------------------------
            # Two Character Operators
            # ---------------------------------------

            two_char = self.current_char

            if self.peek() is not None:
                two_char += self.peek()

            if two_char in DOUBLE_CHAR_TOKENS:

                tokens.append(
                    Token(
                        DOUBLE_CHAR_TOKENS[two_char],
                        two_char,
                        self.line,
                        self.column
                    )
                )

                self.advance()
                self.advance()

                continue

            # ---------------------------------------
            # Single Character Operators
            # ---------------------------------------

            if self.current_char in SINGLE_CHAR_TOKENS:

                tokens.append(
                    Token(
                        SINGLE_CHAR_TOKENS[self.current_char],
                        self.current_char,
                        self.line,
                        self.column
                    )
                )

                self.advance()
                continue

            # ---------------------------------------
            # Unknown Character
            # ---------------------------------------

            raise SyntaxError(
                f"Unknown character '{self.current_char}' "
                f"at line {self.line}, column {self.column}"
            )

        # ---------------------------------------
        # EOF
        # ---------------------------------------

        tokens.append(
            Token(
                TokenType.EOF,
                None,
                self.line,
                self.column
            )
        )

        return tokens