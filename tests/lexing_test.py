import unittest
from enochi.lexer import Lexer


class LexingText(unittest.TestCase):

    def test_lex(self):
        l = Lexer('1')
        print(l)
