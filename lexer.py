import re


(TITLE, SEPARATION, BREAK, ORDER_LIST, UNORDER_LIST,
 STRONG, EMPHASIS, LINK, IMAGE, CODE,
 STRING, NEWLINE, EOF) = \
    ('TITLE', 'SEPARATION', 'BREAK', 'ORDER_LIST', 'UNORDER_LIST',
     'STRONG', 'EMPHASIS', 'LINK', 'IMAGE', 'CODE',
     'STRING', 'NEWLINE', 'EOF')

MARKDOWN_PATTERNS = [
    (r'#+[ \t]+', TITLE),
    (r'\*{3}[ \t]*', SEPARATION),
    (r'[ \t]?\+[ \t]+', UNORDER_LIST),
    (r'[ \t]?\d+\.[ \t]+', ORDER_LIST),
    (r'\*\*[^\*]+\*\*', STRONG),
    (r'\*[^\*]+\*', EMPHASIS),
    (r'!\[.+\]\(.+\)', IMAGE),
    (r'\[.+\]\(.+\)', LINK),
    (r'`{3}[ \t]*', CODE),
    (r'(\n|\r\n)(\n|\r\n)+', BREAK),
    (r'(\n|\r\n)', NEWLINE),
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


def lex(input_text):
    pos = 0
    tokens = []
    not_match = []
    while pos < len(input_text):
        match = None
        for token_expr in MARKDOWN_PATTERNS:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(input_text, pos)
            if match:
                text = match.group(0)
                if tag:
                    if len(not_match) != 0:
                        tokens.append(Token(STRING, ''.join(not_match)))
                    tokens.append(Token(tag, text))
                break
        if not match:
            not_match.append(input_text[pos])
            pos += 1
        else:
            not_match = []
            pos = match.end(0)
    if len(not_match) != 0:
        tokens.append(Token(STRING, ''.join(not_match)))
    return tokens
