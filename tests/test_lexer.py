import unittest

from lexer import *


class TestLexer(unittest.TestCase):
    def test_title_lex(self):
        self.assertEqual(Lexer('# hello').lex(MARKDOWN_PATTERNS),
                         [Token(TITLE, '# '), Token(STRING, 'hello')])
        self.assertEqual(Lexer('## hello world again').lex(MARKDOWN_PATTERNS),
                         [Token(TITLE, '## '), Token(STRING, 'hello world again')])

    def test_order_list_lex(self):
        self.assertEqual(Lexer('1. hello').lex(MARKDOWN_PATTERNS),
                         [Token(ORDER_LIST, '1. '), Token(STRING, 'hello')])

    def test_unorder_list_lex(self):
        self.assertEqual(Lexer('+  hello').lex(MARKDOWN_PATTERNS),
                         [Token(UNORDER_LIST, '+  '), Token(STRING, 'hello')])

    def test_strong_lex(self):
        for a in Lexer('hello **chenbin** again').lex(MARKDOWN_PATTERNS):
            print(a)
        self.assertEqual(Lexer('hello **chenbin** again').lex(MARKDOWN_PATTERNS),
                         [Token(STRING, 'hello '),
                          Token(STRONG, '**chenbin**'),
                          Token(STRING, ' again')])
