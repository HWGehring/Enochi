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


class Lexer:

    def __init__(self, source_code):
        self.source_code = source_code

    def next_token(self, string_index):
        match_text = self.source_code[string_index:]
        token = None
        token_text = None

        for token_def in TokenType.token_defs():
            name, pattern, value_filter = token_def

            if pattern is None:
                continue
            elif isinstance(pattern, str):
                if not match_text.startswith(pattern):
                    continue
                match_value = pattern
            else:
                match = pattern.match(match_text)
                if not match:
                    continue
                match_value = match.group(0)

            if token_text is not None and len(token_text) >= len(match_value):
                continue

            token_text = match_value
            if value_filter is not None:
                match_value = value_filter(match_value)
            token = Token(token_def, match_value, slice(string_index, string_index + len(token_text)))

        return token

    def all_tokens(self):
        string_index = 0
        while string_index < len(self.source_code):
            token = self.next_token(string_index)
            yield token
            string_index = token.slice.stop
