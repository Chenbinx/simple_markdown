from lexer import *
from markdown import *



class Parser(object):
    """Parse tokens which are lexed by lexer
    """
    def __init__(self, text):
        self.tokens = lex(text)
        self.index = 0
        self.current_token = self.tokens[self.index]

    def next_token(self):
        """Move current index forward"""
        self.index += 1
        if self.index == len(self.tokens):
            return Token(EOF, '')
        return self.tokens[self.index]

    def eat(self, token_type):
        """Try to eat token which the token type is equal to token_type"""
        if self.current_token.type == token_type:
            self.current_token = self.next_token()
            return True
        return False

    def consume(self, token_type):
        """Consume a token"""
        if not self.eat(token_type):
            raise Exception('Invalid Syntax')

    def skip_whitespaces(self):
        """Skip whitespaces and newline"""
        while self.current_token.type in [STRING, NEWLINE] and \
              not self.current_token.value.strip():
            self.consume(self.current_token.type)

    def skip_break(self):
        """Skip break tokens"""
        self.eat(BREAK)

    def element(self):
        self.skip_whitespaces()
        token = self.current_token
        node = None
        if token.type == STRING:
            self.consume(STRING)
            node = Raw(token.value)
        elif token.type == STRONG:
            self.consume(STRONG)
            node = Strong(token.value.strip('*'))
        elif token.type == EMPHASIS:
            self.consume(EMPHASIS)
            node = Emphasis(token.value.strip('*'))
        elif token.type == LINK:
            self.consume(LINK)
            name, url = token.value.split('](')
            node = Link(url.strip('()'), name.strip('['))
        elif token.type == IMAGE:
            self.consume(IMAGE)
            name, url = token.value.split('](')
            node = ImageLink(url.strip('()'))
        return node

    def elements(self):
        ret = []
        while self.current_token.type not in [NEWLINE, EOF]:
            element = self.element()
            if element:
                ret.append(element)
            else:
                break
        return Content(*ret)

    def list_items(self):
        ret = []
        order_type = self.current_token.type
        while self.current_token.type == order_type:
            self.consume(self.current_token.type)
            ret.append(self.elements())
            self.skip_whitespaces()
        return ret

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
            content = self.elements()
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
            self.eat(CODE)
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
            return Division(self.elements())

    def parse(self):
        nodes = []
        while self.current_token.type != EOF:
            node = self.paragraph()
            if node:
                nodes.append(node)
        return nodes
