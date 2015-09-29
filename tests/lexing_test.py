import unittest
from enochi.lexer import Lexer
from enochi.token_type import TokenType


class LexingText(unittest.TestCase):

    def test_simple_addition(self):
        l = Lexer('1+1')
        t = l.all_tokens()
        t = list(t)
        first_one = t[0]
        self.assertEqual(first_one.type, TokenType.integer)
        self.assertEqual(first_one.value, 1)
        self.assertEqual(first_one.slice, slice(0, 1, None))

        plus = t[1]
        self.assertEqual(plus.type, TokenType.plus)
        self.assertEqual(plus.value, '+')
        self.assertEqual(plus.slice, slice(1, 2, None))

        second_one = t[2]
        self.assertEqual(second_one.type, TokenType.integer)
        self.assertEqual(second_one.value, 1)
        self.assertEqual(second_one.slice, slice(2, 3, None))

    def test_binary_op(self):
        l = Lexer('(1+1)')
        t = l.all_tokens()
        t = list(t)
        print(t)