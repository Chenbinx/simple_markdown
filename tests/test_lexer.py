import unittest

from lexer import *


class TestLexer(unittest.TestCase):
    def test_title_lex(self):
        self.assertEqual(lex('# hello'),
                         [Token(TITLE, '# '), Token(STRING, 'hello')])
        self.assertEqual(lex('## hello world again'),
                         [Token(TITLE, '## '), Token(STRING, 'hello world again')])

    def test_order_list_lex(self):
        self.assertEqual(lex('1. hello'),
                         [Token(ORDER_LIST, '1. '), Token(STRING, 'hello')])

    def test_unorder_list_lex(self):
        self.assertEqual(lex('+  hello'),
                         [Token(UNORDER_LIST, '+  '), Token(STRING, 'hello')])

    def test_strong_lex(self):
        self.assertEqual(lex('hello **chenbin** again'),
                         [Token(STRING, 'hello '),
                          Token(STRONG, '**chenbin**'),
                          Token(STRING, ' again')])

    def test_emphasis_lex(self):
        self.assertEqual(lex('hello *chenbin* again'),
                         [Token(STRING, 'hello '),
                          Token(EMPHASIS, '*chenbin*'),
                          Token(STRING, ' again')])

    def test_link_lex(self):
        self.assertEqual(lex('hello [link](www.zte.com.cn)'),
                         [Token(STRING, 'hello '),
                          Token(LINK, '[link](www.zte.com.cn)')])

    def test_image_lex(self):
        self.assertEqual(lex('hello ![link](www.zte.com.cn)'),
                         [Token(STRING, 'hello '),
                          Token(IMAGE, '![link](www.zte.com.cn)')])

    def test_code_lex(self):
        self.assertEqual(lex('''```
func() {
    print("hello")
}
```'''),
                         [Token(CODE, '```'),
                          Token(NEWLINE, '\n'),
                          Token(STRING, 'func() {'),
                          Token(NEWLINE, '\n'),
                          Token(STRING, '    print("hello")'),
                          Token(NEWLINE, '\n'),
                          Token(STRING, '}'),
                          Token(NEWLINE, '\n'),
                          Token(CODE, '```')])
