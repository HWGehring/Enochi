from enochi.lexing import TokenType
from enochi import astnodes

__author__ = 'hwgehring'


class ParseError(Exception):

    def __init__(self, message, *tokens):
        self.message = message
        self.tokens = tokens

    def __str__(self):
        if len(self.tokens) == 0:
            return self.message

        return '{0}-{1}: {2}'.format(self.tokens[0].slice.start, self.tokens[-1].slice.stop-1, self.message)


class TokenStack:

    def __init__(self, tokens):
        self._tokens = list(tokens)
        self._cursor = 0
        self._cursor_stack = []

    def peek(self):
        try:
            return self._tokens[self._cursor]
        except IndexError:
            raise ParseError('Unexpected end of input')

    def pop(self):
        rv = self.peek()
        self._cursor += 1
        return rv

    def push_cursor(self):
        self._cursor_stack.append(self._cursor)

    def pop_cursor(self):
        self._cursor = self._cursor_stack.pop()


class ParserBase:

    def __init__(self, token_stack):
        self.token_stack = token_stack
        self.node = self.parse()

    def parse(self):
        raise NotImplementedError()

    def pop_expecting(self, type_):
        next_token = self.token_stack.pop()
        if next_token.type is not type_:
            raise ParseError('Unexpected token: {0}, expected {1}'.format(next_token.type, type_), next_token)
        return next_token


class IntegerLiteralExpression(ParserBase):

    def parse(self):
        int_token = self.pop_expecting(TokenType.integer)
        return astnodes.IntegerLiteral(int_token.value)


class UnaryOpExpression(ParserBase):

    def parse(self):
        op_token = self.token_stack.pop()
        if op_token.type not in [TokenType.plus, TokenType.minus]:
            raise ParseError('Unexpected token: {0}, expected unary operator'.format(op_token.type), op_token)
        rhs_node = Expression(self.token_stack).node
        return astnodes.UnaryOpExpression(op_token.value, rhs_node)


class BinaryOpExpression(ParserBase):

    _op_precedence = {
        '+': 20,
        '-': 20,
        '*': 30,
        '/': 30
    }

    def parse(self):
        primary = PrimaryExpression(self.token_stack)
        return self.parse_expression_(primary, 0)

    def parse_expression_(self, lhs, min_precedence):
        while self.next_is_binary() and self.precedence_() >= min_precedence:
            op_token = self.token_stack
            rhs = PrimaryExpression(self.token_stack)
            while self.next_is_binary() and self.precedence_() > self.precedence_(op_token):
                rhs = self.parse_expression_(rhs, self.precedence_())
            lhs = astnodes.BinaryOpExpression(lhs, op_token.value, rhs)

        return lhs

    def next_is_binary(self):
        next_token = self.token_stack.peek()
        return next_token.value in BinaryOpExpression._op_precedence

    def precedence_(self, token = None):
        token = token or self.token_stack.peek()
        return BinaryOpExpression._op_precedence[token.value]


class BracketedExpression(ParserBase):

    def parse(self):
        self.pop_expecting(TokenType.left_paren)
        expr_node = Expression(self.token_stack).node
        self.pop_expecting(TokenType.right_paren)
        return expr_node


class PrimaryExpression(ParserBase):

    def try_to_parse(self, parser):
        try:
            self.token_stack.push_cursor()
            return parser(self.token_stack).node, True
        except ParseError:
            self.token_stack.pop_cursor()
            return None, False

    def parse(self):
        rv, ok = self.try_to_parse(IntegerLiteralExpression)
        if ok:
            return rv

        rv, ok = self.try_to_parse(UnaryOpExpression)
        if ok:
            return rv

        rv, ok = self.try_to_parse(BracketedExpression)
        if ok:
            return rv

        raise ParseError('Unexpected token: {0}'.format(self.token_stack.peek().type), self.token_stack.peek())

Expression = PrimaryExpression
