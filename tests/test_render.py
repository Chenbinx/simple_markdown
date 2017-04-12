import unittest

from render import Render


class TestRender(unittest.TestCase):
    def test_title_render(self):
        text = '''
# title1
## subtitle1-1
## subtitle1-2
# title2
## subtitle2-1
## subtitle2-2
### subtitle2-2-1
#### subtitle2-2-1-1
##### subtitle2-2-1-1-1
###### subtitle2-2-1-1-1-1
####### subtitle2-2-1-1-1-1-1
'''
        self.assertEqual(Render().render_markdown(text),
                         '<h1>title1</h1><h2>subtitle1-1</h2><h2>subtitle1-2</h2><h1>title2</h1><h2>subtitle2-1</h2><h2>subtitle2-2</h2><h3>subtitle2-2-1</h3><h4>subtitle2-2-1-1</h4><h5>subtitle2-2-1-1-1</h5><h6>subtitle2-2-1-1-1-1</h6><h6>subtitle2-2-1-1-1-1-1</h6>')

    def test_order_list_render(self):
        text = '''
 1. chapter1
 2. chapter2

 3. chapter3
'''
        self.assertEqual(Render().render_markdown(text),
                         '<ol><li>chapter1</li><li>chapter2</li><li>chapter3</li></ol>')

    def test_unorder_list_render(self):
        text = '''
 +  chapter1

 + chapter2

 + chapter3
'''
        self.assertEqual(Render().render_markdown(text),
                         '<ul><li>chapter1</li><li>chapter2</li><li>chapter3</li></ul>')

    def test_code_render(self):
        text = '''
```
class Token(object):
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

    def __str__(self):
        return 'Token({type}: {value})'.format(
            type=self.type,
            value=self.value)

    def __eq__(self, rhs):
        return self.type == rhs.type and self.value == rhs.value
```
'''
        self.assertEqual(Render().render_markdown(text),
                         '''<pre>
class Token(object):
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

    def __str__(self):
        return 'Token({type}: {value})'.format(
            type=self.type,
            value=self.value)

    def __eq__(self, rhs):
        return self.type == rhs.type and self.value == rhs.value
</pre>''')

    def test_link_sep_image_link_render(self):
        text = '''
[zte](http://www.zte.com.cn)
***
![zte_logo](http://www.zte.com.cn/logo.png)
'''
        self.assertEqual(Render().render_markdown(text),
                         '<div><a href="http://www.zte.com.cn">zte</a></div><hr><div><img src="http://www.zte.com.cn/logo.png"></div>')

    def test_rich_title_and_contents(self):
        text = '''
# the *whole* new feature

1. [chapter1](#chapter1)
2. [chapter2](#chapter2)

We're happy to announce the latest course for raywenderlich.com subscribers - an update to our Beginning iOS Animations course!

In this course, *you'll* learn how to create delightful animations for your iOS apps. Along the way, you'll learn **about** Auto *Layout* constraint [hello](http://www.zte.com.cn) animations, view controller transitions, troubleshooting animations gone wrong, and more!
'''
        self.assertEqual(Render().render_markdown(text),
                         '''<h1>the <em>whole</em> new feature</h1><ol><li><a href="#chapter1">chapter1</a></li><li><a href="#chapter2">chapter2</a></li></ol><div>We're happy to announce the latest course for raywenderlich.com subscribers - an update to our Beginning iOS Animations course!</div><br><div>In this course, <em>you'll</em> learn how to create delightful animations for your iOS apps. Along the way, you'll learn <strong>about</strong> Auto <em>Layout</em> constraint <a href="http://www.zte.com.cn">hello</a> animations, view controller transitions, troubleshooting animations gone wrong, and more!</div>''')
