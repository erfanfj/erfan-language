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
    UnaryOperation,
    Block,
    IfStatement,
    FunctionDef,
    ReturnStatement,
    ClassDef,
    This,
    MemberAccess,
    MethodCall,
    ArrayLiteral,
    IndexAccess,
    ForInStatement,
    WhileStatement,
    BreakStatement,
    ContinueStatement,
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

    def block(self):

        statements = []

        self.eat(TokenType.LBRACE)

        while (
            self.current.type != TokenType.RBRACE
            and self.current.type != TokenType.EOF
        ):

            if self.current.type == TokenType.NEWLINE:
                self.advance()
                continue

            statements.append(
                self.statement()
            )

            while self.current.type == TokenType.NEWLINE:
                self.advance()

        self.eat(TokenType.RBRACE)

        return Block(statements)

    def class_block(self):

        methods = []

        self.eat(TokenType.LBRACE)

        while (
            self.current.type != TokenType.RBRACE
            and self.current.type != TokenType.EOF
        ):

            if self.current.type == TokenType.NEWLINE:
                self.advance()
                continue

            if self.current.type != TokenType.FN:
                raise SyntaxError("Class body may only contain method definitions")

            methods.append(self.function_definition())

            while self.current.type == TokenType.NEWLINE:
                self.advance()

        self.eat(TokenType.RBRACE)

        return methods

    def if_statement(self):

        self.eat(TokenType.IF)

        condition = self.expression()

        while self.current.type == TokenType.NEWLINE:
            self.advance()

        then_block = self.block()

        while self.current.type == TokenType.NEWLINE:
            self.advance()

        else_block = None

        if self.current.type == TokenType.ELSE:

            self.eat(TokenType.ELSE)

            while self.current.type == TokenType.NEWLINE:
                self.advance()

            else_block = self.block()

        return IfStatement(
            condition=condition,
            then_block=then_block,
            else_block=else_block
        )

    def for_in_statement(self):

        self.eat(TokenType.BORO)

        variable = self.current.value

        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.ROYE)

        iterable = self.expression()

        while self.current.type == TokenType.NEWLINE:
            self.advance()

        body = self.block()

        return ForInStatement(variable, iterable, body)

    def while_statement(self):

        self.eat(TokenType.WHILE)

        condition = self.expression()

        while self.current.type == TokenType.NEWLINE:
            self.advance()

        body = self.block()

        return WhileStatement(condition, body)

    def statement(self):

        if self.current.type == TokenType.CLASS:
            return self.class_definition()

        if self.current.type == TokenType.FN:
            return self.function_definition()

        if self.current.type == TokenType.RETURN:
            return self.return_statement()

        if self.current.type == TokenType.BORO:
            return self.for_in_statement()

        if self.current.type == TokenType.WHILE:
            return self.while_statement()

        if self.current.type == TokenType.BREAK:
            self.advance()
            return BreakStatement()

        if self.current.type == TokenType.CONTINUE:
            self.advance()
            return ContinueStatement()

        if self.current.type == TokenType.IDENTIFIER:

            next_type = self.tokens[self.position + 1].type

            if next_type == TokenType.ASSIGN:
                return self.assignment()

            if next_type == TokenType.LPAREN:
                return self.function_call()

            if next_type in (TokenType.DOT, TokenType.LBRACKET):
                return self.postfix_statement()

        if self.current.type == TokenType.THIS:

            return self.postfix_statement()

        if self.current.type == TokenType.CHAP:
            return self.function_call()

        if self.current.type == TokenType.IF:
            return self.if_statement()

        raise SyntaxError("Unknown Statement")

    # -----------------------------------------------------

    def class_definition(self):

        self.eat(TokenType.CLASS)

        name = self.current.value

        self.eat(TokenType.IDENTIFIER)

        while self.current.type == TokenType.NEWLINE:
            self.advance()

        methods = self.class_block()

        return ClassDef(name, methods)

    def function_definition(self):

        self.eat(TokenType.FN)

        name = self.current.value

        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.LPAREN)

        params = []

        if self.current.type != TokenType.RPAREN:

            params.append(self.current.value)

            self.eat(TokenType.IDENTIFIER)

            while self.current.type == TokenType.COMMA:

                self.eat(TokenType.COMMA)

                params.append(self.current.value)

                self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.RPAREN)

        while self.current.type == TokenType.NEWLINE:
            self.advance()

        body = self.block()

        return FunctionDef(name, params, body)

    def return_statement(self):

        self.eat(TokenType.RETURN)

        value = self.expression()

        return ReturnStatement(value)

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

    def postfix_statement(self):

        node = self.postfix()

        if self.current.type == TokenType.ASSIGN:

            self.eat(TokenType.ASSIGN)

            value = self.expression()

            return Assignment(node, value)

        if isinstance(node, (MethodCall, FunctionCall)):
            return node

        raise SyntaxError("Invalid statement")

    # -----------------------------------------------------

    def function_call(self):

        func = self.current.value

        if self.current.type == TokenType.CHAP:
            self.eat(TokenType.CHAP)
        else:
            self.eat(TokenType.IDENTIFIER)

        args = self.parse_call_args()

        return FunctionCall(func, args)

    def parse_call(self, name):

        args = self.parse_call_args()

        return FunctionCall(name, args)

    def parse_call_args(self):

        self.eat(TokenType.LPAREN)

        args = []

        if self.current.type != TokenType.RPAREN:

            args.append(self.expression())

            while self.current.type == TokenType.COMMA:

                self.eat(TokenType.COMMA)

                args.append(self.expression())

        self.eat(TokenType.RPAREN)

        return args

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
            TokenType.PERCENT,
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

        return self.postfix()

    def postfix(self):

        node = self.primary()

        while True:

            if self.current.type == TokenType.DOT:

                self.advance()

                member = self.current.value

                self.eat(TokenType.IDENTIFIER)

                if self.current.type == TokenType.LPAREN:

                    args = self.parse_call_args()

                    node = MethodCall(node, member, args)

                else:

                    node = MemberAccess(node, member)

            elif self.current.type == TokenType.LBRACKET:

                self.advance()

                index = self.expression()

                self.eat(TokenType.RBRACKET)

                node = IndexAccess(node, index)

            else:

                break

        return node

    def array_literal(self):

        self.eat(TokenType.LBRACKET)

        elements = []

        if self.current.type != TokenType.RBRACKET:

            elements.append(self.expression())

            while self.current.type == TokenType.COMMA:

                self.eat(TokenType.COMMA)

                elements.append(self.expression())

        self.eat(TokenType.RBRACKET)

        return ArrayLiteral(elements)

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

        if token.type == TokenType.THIS:

            self.advance()

            return This()

        if token.type == TokenType.IDENTIFIER:

            if self.tokens[self.position + 1].type == TokenType.LPAREN:

                name = token.value

                self.advance()

                return self.parse_call(name)

            self.advance()

            return Identifier(token.value)

        if token.type == TokenType.LBRACKET:

            return self.array_literal()

        if token.type == TokenType.LPAREN:

            self.advance()

            node = self.expression()

            self.eat(TokenType.RPAREN)

            return node

        raise SyntaxError(
            f"Unexpected token {token.type.name}"
        )
