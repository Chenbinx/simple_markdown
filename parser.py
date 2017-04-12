from lexer import *
from markdown import *


class Parser(object):
    def __init__(self, text):
        self.tokens = lex(text)
        self.index = 0
        self.current_token = self.tokens[self.index]

    def error(self):
        raise Exception('Invalid Syntax')

    def next_token(self):
        self.index += 1
        if self.index == len(self.tokens):
            return Token(EOF, '')
        return self.tokens[self.index]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.next_token()
            return True
        return False

    def consume(self, token_type):
        if not self.eat(token_type):
            self.error()

    def skip_whitespaces(self):
        while self.current_token.type in [STRING, NEWLINE] and \
              not self.current_token.value.strip():
            self.consume(self.current_token.type)

    def skip_break(self):
        self.eat(BREAK)

    def element(self):
        self.skip_whitespaces()
        token = self.current_token
        if token.type == STRING:
            self.consume(STRING)
            return Raw(token.value)
        elif token.type == STRONG:
            self.consume(STRONG)
            return Strong(token.value.strip('*'))
        elif token.type == EMPHASIS:
            self.consume(EMPHASIS)
            return Emphasis(token.value.strip('*'))
        elif token.type == LINK:
            self.consume(LINK)
            name, url = token.value.split('](')
            return Link(url.strip('()'), name.strip('['))
        elif token.type == IMAGE:
            self.consume(IMAGE)
            name, url = token.value.split('](')
            return ImageLink(url.strip('()'))
        else:
            return None

    def group(self):
        g = []
        while self.current_token.type not in [NEWLINE, EOF]:
            element = self.element()
            if element:
                g.append(element)
            else:
                break
        return Content(*g)

    def list_items(self):
        g = []
        token = self.current_token
        order_type = token.type
        while token.type == order_type:
            self.consume(token.type)
            g.append(self.group())
            self.skip_whitespaces()
            token = self.current_token
        return g

    def source_code(self):
        codes = []
        while self.current_token.type not in [CODE, EOF]:
            codes.append(Raw(self.current_token.value))
            self.current_token = self.next_token()
        return Content(*codes)

    def paragraph(self):
        self.skip_whitespaces()
        token = self.current_token
        if token.type == TITLE:
            self.consume(TITLE)
            level = len(token.value.strip())
            content = self.group()
            self.skip_break()
            return Title(level, content)
        elif token.type in [ORDER_LIST, UNORDER_LIST]:
            list_items = self.list_items()
            ordered = True if token.type == ORDER_LIST else False
            self.skip_break()
            return ListItems(ordered, *list_items)
        elif token.type == CODE:
            self.consume(CODE)
            source_code = self.source_code()
            self.consume(CODE)
            self.skip_break()
            return Code(source_code)
        elif token.type == SEPARATION:
            self.consume(SEPARATION)
            self.skip_break()
            return Separation()
        elif token.type == BREAK:
            self.consume(BREAK)
            return Break()
        else:
            return Division(self.group())

    def parse(self):
        nodes = []
        while self.current_token.type != EOF:
            node = self.paragraph()
            if node:
                nodes.append(node)
        return nodes
