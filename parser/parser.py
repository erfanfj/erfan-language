from lexer.token import TokenType

from erfan_ast.nodes import (
    Program,
    Assignment,
    Identifier,
    Number,
    Float,
    String,
    Boolean,
    Null,
    BinaryOperation,
    FunctionCall,
    UnaryOperation
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

        if self.current.type != TokenType.RPAREN:

            args.append(self.expression())

            while self.current.type == TokenType.COMMA:

                self.eat(TokenType.COMMA)

                args.append(self.expression())

        self.eat(TokenType.RPAREN)

        return FunctionCall(func, args)

    # -----------------------------------------------------

    def expression(self):
        return self.logical_or()
    
    def logical_or(self):

        node = self.logical_and()

        while self.current.type == TokenType.OR:

            op = self.current.value

            self.advance()

            node = BinaryOperation(
                node,
                op,
                self.logical_and()
            )

        return node


    def logical_and(self):

        node = self.equality()

        while self.current.type == TokenType.AND:

            op = self.current.value

            self.advance()

            node = BinaryOperation(
                node,
                op,
                self.equality()
            )

        return node
    
    def equality(self):

        node = self.comparison()

        while self.current.type in (
            TokenType.EQ,
            TokenType.NE,
        ):

            op = self.current.value

            self.advance()

            node = BinaryOperation(
                node,
                op,
                self.comparison()
            )

        return node
    
    def comparison(self):

        node = self.addition()

        while self.current.type in (

            TokenType.GT,
            TokenType.LT,
            TokenType.GTE,
            TokenType.LTE,

        ):

            op = self.current.value

            self.advance()

            node = BinaryOperation(
                node,
                op,
                self.addition()
            )

        return node
    
    def addition(self):

        node = self.multiplication()

        while self.current.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):

            op = self.current.value

            self.advance()

            node = BinaryOperation(
                node,
                op,
                self.multiplication()
            )

        return node
    
    def multiplication(self):

        node = self.unary()

        while self.current.type in (
            TokenType.STAR,
            TokenType.SLASH,
        ):

            op = self.current.value

            self.advance()

            node = BinaryOperation(
                node,
                op,
                self.unary()
            )

        return node
    
    def unary(self):

        if self.current.type in (

            TokenType.NOT,
            TokenType.MINUS,
            TokenType.PLUS,

        ):

            op = self.current.value

            self.advance()

            return UnaryOperation(
                op,
                self.unary()
            )

        return self.primary()


    # -----------------------------------------------------

    def primary(self):

        token = self.current

        if token.type == TokenType.NUMBER:

            self.advance()

            return Number(token.value)

        if token.type == TokenType.FLOAT:

            self.advance()

            return Float(token.value)

        if token.type == TokenType.STRING:

            self.advance()

            return String(token.value)

        if token.type == TokenType.TRUE:

            self.advance()

            return Boolean(True)

        if token.type == TokenType.FALSE:

            self.advance()

            return Boolean(False)

        if token.type == TokenType.NULL:

            self.advance()

            return Null()

        if token.type == TokenType.IDENTIFIER:

            self.advance()

            return Identifier(token.value)

        if token.type == TokenType.LPAREN:

            self.advance()

            node = self.expression()

            self.eat(TokenType.RPAREN)

            return node

        raise SyntaxError(
            f"Unexpected token {token.type.name}"
    )