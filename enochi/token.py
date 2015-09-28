from collections import namedtuple
import re

__author__ = 'hwgehring'

Token = namedtuple('Token', ('type', 'value', 'slice'))


class TokenDef(namedtuple('TokenDef', ['name', 'pattern', 'value_filter'])):
    def __repr__(self):
        return 'TokenType.' + self.name


class TokenType:

    plus = TokenDef('plus', '+', None)
    minus = TokenDef('minus', '-', None)
    asterisk = TokenDef('asterisk', '*', None)
    slash = TokenDef('slash', '/', None)

    left_paren = TokenDef('left_paren', '(', None)
    right_paren = TokenDef('right_paren', ')', None)

    integer = TokenDef('integer', re.compile('[0-9]+'), int)
    whitespace = TokenDef('whitespace', re.compile('[ \t]+'), None)

    @classmethod
    def token_defs(cls):
        for prop in dir(TokenType):
            if prop.startswith('__') or prop == 'token_defs':
                continue
            yield getattr(TokenType, prop)
