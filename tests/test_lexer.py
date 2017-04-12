import unittest

from lexer import *


class TestLexer(unittest.TestCase):
    def test_title_lex(self):
        self.assertEqual(Lexer('# hello').lex(),
                         [Token(TITLE, '# '), Token(STRING, 'hello')])
        self.assertEqual(Lexer('## hello world again').lex(),
                         [Token(TITLE, '## '), Token(STRING, 'hello world again')])

    def test_order_list_lex(self):
        self.assertEqual(Lexer('1. hello').lex(),
                         [Token(ORDER_LIST, '1. '), Token(STRING, 'hello')])

    def test_unorder_list_lex(self):
        self.assertEqual(Lexer('+  hello').lex(),
                         [Token(UNORDER_LIST, '+  '), Token(STRING, 'hello')])

    def test_strong_lex(self):
        self.assertEqual(Lexer('hello **chenbin** again').lex(),
                         [Token(STRING, 'hello '),
                          Token(STRONG, '**chenbin**'),
                          Token(STRING, ' again')])

    def test_emphasis_lex(self):
        self.assertEqual(Lexer('hello *chenbin* again').lex(),
                         [Token(STRING, 'hello '),
                          Token(EMPHASIS, '*chenbin*'),
                          Token(STRING, ' again')])

    def test_link_lex(self):
        self.assertEqual(Lexer('hello [link](www.zte.com.cn)').lex(),
                         [Token(STRING, 'hello '),
                          Token(LINK, '[link](www.zte.com.cn)')])

    def test_image_lex(self):
        self.assertEqual(Lexer('hello ![link](www.zte.com.cn)').lex(),
                         [Token(STRING, 'hello '),
                          Token(IMAGE, '![link](www.zte.com.cn)')])

    def test_code_lex(self):
        self.assertEqual(Lexer('''```
func() {
    print("hello")
}
```''').lex(),
                         [Token(CODE, '```'),
                          Token(NEWLINE, '\n'),
                          Token(STRING, 'func() {'),
                          Token(NEWLINE, '\n'),
                          Token(STRING, '    print("hello")'),
                          Token(NEWLINE, '\n'),
                          Token(STRING, '}'),
                          Token(NEWLINE, '\n'),
                          Token(CODE, '```')])
