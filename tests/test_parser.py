import unittest

from parser import *


class TestParser(unittest.TestCase):
    def test_parser_strong(self):
        self.assertEqual(str(Parser('**chenbin**').element()),
                         '<strong>chenbin</strong>')

    def test_parser_title(self):
        self.assertEqual(str(Parser('## hello 2 **hello** a *em*').paragraph()),
                         '<h2>hello 2 <strong>hello</strong> a <em>em</em></h2>')

    def test_parser_empty_title(self):
        self.assertEqual(str(Parser('## ').paragraph()), '## ')
        self.assertEqual(str(Parser('##').paragraph()), '<div>##</div>')

    def test_parser_list(self):
        self.assertEqual(str(Parser('''+ chap1\n+ chap2*hi*''').paragraph()),
                         '<ul><li>chap1</li><li>chap2<em>hi</em></li></ul>')

    def test_parser_empty_list(self):
        self.assertEqual(str(Parser('''+ ''').paragraph()), '+ ')
        self.assertEqual(str(Parser('''+''').paragraph()), '<div>+</div>')
        self.assertEqual(str(Parser('''1. ''').paragraph()), '1. ')
        self.assertEqual(str(Parser('''1.''').paragraph()), '<div>1.</div>')

    def test_parser_link(self):
        self.assertEqual(str(Parser('[zte](http://www.zte.com.cn)').paragraph()),
                         '<div><a href="http://www.zte.com.cn">zte</a></div>')
        self.assertEqual(str(Parser('![zte](http://www.zte.com.cn/logo.png)').paragraph()),
                         '<div><img src="http://www.zte.com.cn/logo.png"></div>')

    def test_parser_assemble(self):
        self.assertEqual(str(Parser('**chenbin**hello').paragraph()),
                         '<div><strong>chenbin</strong>hello</div>')

    def test_parser_code(self):
        self.assertEqual(str(Parser('''```
# comment 1
# comment 2
func() {
    print('hello')
}
```
''').paragraph()),
                         '''<pre>
# comment 1
# comment 2
func() {
    print('hello')
}
</pre>''')
