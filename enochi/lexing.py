from collections import namedtuple
import re

__author__ = 'hwgehring'


Token = namedtuple('Token', ('type', 'value', 'slice'))


class TokenDef(namedtuple('TokenDef', ['name', 'pattern', 'value_filter'])):
    def __repr__(self):
        return 'TokenType.' + self.name


class TokenType:

    defs = [
        TokenDef('plus', '+', None),
        TokenDef('minus', '-', None),
        TokenDef('asterisk', '*', None),
        TokenDef('slash', '/', None),

        TokenDef('left_paren', '(', None),
        TokenDef('right_paren', ')', None),

        TokenDef('integer', re.compile('[0-9]+'), int),
        TokenDef('whitespace', re.compile('[ \t]+'), None),
    ]

for def_ in TokenType.defs:
    setattr(TokenType, def_.name, def_)


def first_token(text, start=0):
    match_text = text[start:]
    token = None
    token_text = None

    for type_ in TokenType.defs:
        name, pattern, value_filter = type_
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
        token = Token(type_, match_value, slice(start, start + len(token_text)))

    return token


def lex_raw(text):
    start = 0
    while True:
        if start >= len(text):
            break

        token = first_token(text, start)
        yield token
        start = token.slice.stop


def lex_skip_whitespace(text):
    for token in lex_raw(text):
        if token.type is TokenType.whitespace:
            continue
        yield token

lex = lex_skip_whitespace
