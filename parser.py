from lexer import *
from markdown import *


class Parser(object):
    """Parse tokens which are lexed by lexer
    """
    def __init__(self, text):
        self.tokens = lex(text)
        self.index = 0
        self.current_token = self.tokens[self.index]

    def _next_token(self):
        """Move current index forward"""
        self.index += 1
        if self.index == len(self.tokens):
            return Token(EOF, '')
        return self.tokens[self.index]

    def _eat(self, token_type):
        """Try to eat token which the token type is equal to token_type"""
        if self.current_token.type == token_type:
            self.current_token = self._next_token()
            return True
        return False

    def _consume(self, token_type):
        """Consume a token"""
        if not self._eat(token_type):
            raise Exception('Invalid Syntax')

    def _skip_whitespaces(self):
        """Skip whitespaces and newline"""
        while self.current_token.type in [STRING, NEWLINE] and \
              not self.current_token.value.strip():
            self._consume(self.current_token.type)

    def _skip_break(self):
        """Skip break tokens"""
        self._eat(BREAK)

    def _parse_string(self, token):
        self._consume(STRING)
        return Raw(token.value)

    def _parse_strong(self, token):
        self._consume(STRONG)
        return Strong(token.value.strip('*'))

    def _parse_emphasis(self, token):
        self._consume(EMPHASIS)
        return Emphasis(token.value.strip('*'))

    def _parse_link(self, token):
        self._consume(LINK)
        name, url = token.value.split('](')
        return Link(url.strip('()'), name.strip('['))

    def _parse_image_link(self, token):
        self._consume(IMAGE)
        name, url = token.value.split('](')
        return ImageLink(url.strip('()'))

    def _noop(self, token):
        return None

    def _parse_title(self, token):
        self._consume(TITLE)
        level = len(token.value.strip())
        content = self.elements()
        if not content:
            return Raw(token.value)
        self._skip_break()
        return Title(level, content)

    def _list_items(self):
        ret = []
        order_type = self.current_token.type
        while self.current_token.type == order_type:
            self._consume(self.current_token.type)
            elements = self.elements()
            if elements:
                ret.append(elements)
            self._skip_whitespaces()
            self._skip_break()
        return ret

    def _parse_list_items(self, token):
        list_items = self._list_items()
        if not list_items:
            return Raw(token.value)
        ordered = True if token.type == ORDER_LIST else False
        self._skip_break()
        return ListItems(ordered, *list_items)

    def _source_code(self):
        codes = []
        while self.current_token.type not in [CODE, EOF]:
            codes.append(Raw(self.current_token.value))
            self.current_token = self._next_token()
        return Content(*codes)

    def _parse_code(self, token):
        self._consume(CODE)
        source_code = self._source_code()
        self._eat(CODE)
        self._skip_break()
        return Code(source_code)

    def _parse_separation(self, token):
        self._consume(SEPARATION)
        self._skip_break()
        return Separation()

    def _parse_break(self, token):
        self._consume(BREAK)
        return Break()

    def _parse_division(self, token):
        elements = self.elements()
        return Division(elements) if elements else None

    def element(self):
        self._skip_whitespaces()
        token = self.current_token
        func_dict = {
            STRING: self._parse_string,
            STRONG: self._parse_strong,
            EMPHASIS: self._parse_emphasis,
            LINK: self._parse_link,
            IMAGE: self._parse_image_link,
        }
        fn = func_dict.get(token.type, self._noop)
        return fn(token)

    def elements(self):
        ret = []
        while self.current_token.type not in [NEWLINE, EOF]:
            element = self.element()
            if element:
                ret.append(element)
            else:
                break
        return Content(*ret) if ret else None

    def paragraph(self):
        self._skip_whitespaces()
        token = self.current_token
        func_dict = {
            TITLE: self._parse_title,
            ORDER_LIST: self._parse_list_items,
            UNORDER_LIST: self._parse_list_items,
            CODE: self._parse_code,
            SEPARATION: self._parse_separation,
            BREAK: self._parse_break,
        }
        fn = func_dict.get(token.type, self._parse_division)
        return fn(token)

    def parse(self):
        nodes = []
        while self.current_token.type != EOF:
            node = self.paragraph()
            if node:
                nodes.append(node)
        return nodes
