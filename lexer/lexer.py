from .token import Token, TokenType
from .keywords import KEYWORDS


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

        while self.current_char is not None and self.current_char.isdigit():
            value += self.current_char
            self.advance()

        return Token(
            TokenType.NUMBER,
            int(value),
            self.line,
            start
        )

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

        token_type = KEYWORDS.get(
            value,
            TokenType.IDENTIFIER
        )

        return Token(
            token_type,
            value,
            self.line,
            start
        )

    def tokenize(self):

        tokens = []

        while self.current_char is not None:

            if self.current_char in " \t\r":
                self.skip_whitespace()
                continue

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

            if self.current_char.isdigit():
                tokens.append(self.number())
                continue

            if self.current_char.isalpha() or self.current_char == "_":
                tokens.append(self.identifier())
                continue

            if self.current_char == "<" and self.peek() == "-":
                tokens.append(
                    Token(
                        TokenType.ASSIGN,
                        "<-",
                        self.line,
                        self.column
                    )
                )
                self.advance()
                self.advance()
                continue

            if self.current_char == "+":
                tokens.append(
                    Token(
                        TokenType.PLUS,
                        "+",
                        self.line,
                        self.column
                    )
                )
                self.advance()
                continue

            if self.current_char == "-":
                tokens.append(
                    Token(
                        TokenType.MINUS,
                        "-",
                        self.line,
                        self.column
                    )
                )
                self.advance()
                continue

            if self.current_char == "*":
                tokens.append(
                    Token(
                        TokenType.STAR,
                        "*",
                        self.line,
                        self.column
                    )
                )
                self.advance()
                continue

            if self.current_char == "/":
                tokens.append(
                    Token(
                        TokenType.SLASH,
                        "/",
                        self.line,
                        self.column
                    )
                )
                self.advance()
                continue

            if self.current_char == "(":
                tokens.append(
                    Token(
                        TokenType.LPAREN,
                        "(",
                        self.line,
                        self.column
                    )
                )
                self.advance()
                continue

            if self.current_char == ")":
                tokens.append(
                    Token(
                        TokenType.RPAREN,
                        ")",
                        self.line,
                        self.column
                    )
                )
                self.advance()
                continue

            raise SyntaxError(
                f"Unknown character '{self.current_char}' "
                f"at line {self.line}, column {self.column}"
            )

        tokens.append(
            Token(
                TokenType.EOF,
                None,
                self.line,
                self.column
            )
        )

        return tokens