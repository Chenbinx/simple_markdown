import re
import sys


(TITLE, ORDER_LIST, UNORDER_LIST, STRONG, EMPHASIS, STRING) = \
    ('TITLE', 'ORDER_LIST', 'UNORDER_LIST', 'STRONG', 'EMPHASIS', 'STRING')

MARKDOWN_PATTERNS = [
    (r'^#+\s+', TITLE),
    (r'^\s?\+\s+', UNORDER_LIST),
    (r'^\s?[0-9]+\.\s+', ORDER_LIST),
    (r'\*\*[^\*]+\*\*', STRONG),
    # (r'\*[^\*]+*', EMPHASIS),
]


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


class Lexer(object):
    def __init__(self, text):
        self.text = text

    def lex(self, patterns):
        """
        patterns params list
        """
        pos = 0
        tokens = []
        not_match = []
        while pos < len(self.text):
            match = None            
            for token_expr in patterns:
                pattern, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(self.text, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        if len(not_match) != 0:
                            tokens.append(Token(STRING, ''.join(not_match)))
                        tokens.append(Token(tag, text))
                    break
            if not match:
                not_match.append(self.text[pos])
                pos += 1
            else:
                not_match = []
                pos = match.end(0)
        if len(not_match) != 0:
            tokens.append(Token(STRING, ''.join(not_match)))
        return tokens
