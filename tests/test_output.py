#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode:python -*-
# Filename: test_output.py
# Author:   Chenbin
# Time-stamp: <2017-04-12 Wed 22:18:25>

import unittest

from markdown import *


class TestSimpleRender(unittest.TestCase):
    def test_render_raw(self):
        self.assertEqual('hello world', str(Content('hello world')))

    def test_render_title(self):
        self.assertEqual('<h1>hello</h1>', str(Title(1, 'hello')))
        self.assertEqual('<h1>hello</h1>', str(Title(0, 'hello')))
        self.assertEqual('<h6>hello</h6>', str(Title(6, 'hello')))
        self.assertEqual('<h6>hello</h6>', str(Title(7, 'hello')))

    def test_render_division(self):
        self.assertEqual('<div>hello</div>', str(Division('hello')))

    def test_render_separation(self):
        self.assertEqual('<hr>', str(Separation()))

    def test_render_strong(self):
        self.assertEqual('<strong>hello</strong>', str(Strong('hello')))

    def test_render_em(self):
        self.assertEqual('<em>hello</em>', str(Emphasis('hello')))

    def test_render_list(self):
        self.assertEqual('<ol><li>chap1</li><li>chap2</li><li>chap3</li></ol>',
                         str(ListItems(True, 'chap1', 'chap2', 'chap3')))
        self.assertEqual('<ul><li>chap1</li><li>chap2</li><li>chap3</li></ul>',
                         str(ListItems(False, 'chap1', 'chap2', 'chap3')))

    def test_render_url(self):
        self.assertEqual('<a href="http://www.zte.com.cn">ZTE</a>',
                         str(Link('http://www.zte.com.cn', 'ZTE')))

    def test_render_image_url(self):
        self.assertEqual('<img src="http://www.zte.com.cn/logo.png">',
                         str(ImageLink('http://www.zte.com.cn/logo.png')))

    def test_render_code(self):
        self.assertEqual('''<pre>
function test() {
    alert(12)
}
</pre>''',
                         str(Code('''
function test() {
    alert(12)
}
''')))

    def test_multi_render(self):
        self.assertEqual("<h1>hello <em>chenbin's </em>world</h1>",
                         str(Title(1, Content('hello ',
                                              Emphasis("chenbin's "),
                                              'world'))))
