import unittest
from enochi.lexer import TokenType, Token, lex


class LexingText(unittest.TestCase):

    def test_lex(self):
        a = list(lex('1'))[0]
        self.assertEqual(a.type, TokenType.integer)
        self.assertEqual(a.value, 1)
        self.assertEqual(type(a), Token)
