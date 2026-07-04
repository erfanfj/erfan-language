from lexer.token import TokenType

from erfan_ast.nodes import (
    Program,
    Assignment,
    Identifier,
    Number,
    BinaryOperation,
    FunctionCall,
)


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.position = 0
        self.current = self.tokens[self.position]

    # -----------------------------------------------------

    def advance(self):

        self.position += 1

        if self.position < len(self.tokens):
            self.current = self.tokens[self.position]

    # -----------------------------------------------------

    def eat(self, token_type):

        if self.current.type == token_type:
            self.advance()
        else:
            raise SyntaxError(
                f"Expected {token_type.name} "
                f"but got {self.current.type.name}"
            )

    # -----------------------------------------------------

    def parse(self):

        statements = []

        while self.current.type != TokenType.EOF:

            if self.current.type == TokenType.NEWLINE:
                self.advance()
                continue

            statements.append(self.statement())

        return Program(statements)

    # -----------------------------------------------------

    def statement(self):

        if self.current.type == TokenType.IDENTIFIER:

            if self.tokens[self.position + 1].type == TokenType.ASSIGN:
                return self.assignment()

        if self.current.type == TokenType.CHAP:
            return self.function_call()

        raise SyntaxError("Unknown Statement")

    # -----------------------------------------------------

    def assignment(self):

        name = self.current.value

        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.ASSIGN)

        value = self.expression()

        return Assignment(
            Identifier(name),
            value
        )

    # -----------------------------------------------------

    def function_call(self):

        func = self.current.value

        self.eat(TokenType.CHAP)

        self.eat(TokenType.LPAREN)

        args = []

        args.append(
            self.expression()
        )

        self.eat(TokenType.RPAREN)

        return FunctionCall(
            func,
            args
        )

    # -----------------------------------------------------

    def expression(self):

        node = self.term()

        while self.current.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):

            op = self.current.value

            self.advance()

            node = BinaryOperation(
                node,
                op,
                self.term()
            )

        return node

    # -----------------------------------------------------

    def term(self):

        node = self.factor()

        while self.current.type in (
            TokenType.STAR,
            TokenType.SLASH,
        ):

            op = self.current.value

            self.advance()

            node = BinaryOperation(
                node,
                op,
                self.factor()
            )

        return node

    # -----------------------------------------------------

    def factor(self):

        token = self.current

        if token.type == TokenType.NUMBER:

            self.advance()

            return Number(token.value)

        if token.type == TokenType.IDENTIFIER:

            self.advance()

            return Identifier(token.value)

        if token.type == TokenType.LPAREN:

            self.advance()

            node = self.expression()

            self.eat(TokenType.RPAREN)

            return node

        raise SyntaxError("Invalid Expression")