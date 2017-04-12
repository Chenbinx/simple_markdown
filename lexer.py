import re


(TITLE, ORDER_LIST, UNORDER_LIST, STRONG, EMPHASIS,
 LINK, IMAGE, CODE, STRING, NEWLINE) = \
    ('TITLE', 'ORDER_LIST', 'UNORDER_LIST', 'STRONG', 'EMPHASIS',
     'LINK', 'IMAGE', 'CODE', 'STRING', 'NEWLINE')

MARKDOWN_PATTERNS = [
    (r'#+[ \t]+', TITLE),
    (r'[ \t]?\+[ \t]+', UNORDER_LIST),
    (r'[ \t]?\d+\.[ \t]+', ORDER_LIST),
    (r'\*\*[^\*]+\*\*', STRONG),
    (r'\*[^\*]+\*', EMPHASIS),
    (r'!\[.+\]\(.+\)', IMAGE),
    (r'\[.+\]\(.+\)', LINK),
    (r'`{3}[ \t]*', CODE),
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


class Lexer(object):
    def __init__(self, text):
        self.text = text

    def lex(self):
        pos = 0
        tokens = []
        not_match = []
        while pos < len(self.text):
            match = None
            for token_expr in MARKDOWN_PATTERNS:
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


def main():
    r = Lexer('''
# Windows comp

    + [intro](#1)
    + [hello](#2)
    + [chap](#3)
    + [ref](#3)

1. hello
2. world

## <h2 id="1">intro</h2>

    introduce the production

example:

```
guard @check voiagent else {
    @svn checkout http://xx.xx.x.xxx/svn/ZXCCP-VPlat_xxxx/trunk/source.repo/src/vx.x/windows/voiagent/
}
```

PROJECT_DIR = @search_file_path voiagent.sln
OUTPUT_DIR = $PROJECT_DIR\Output\
INSTALLER_DIR = @search_file_path voi_windows_client_setup.nsi
''').lex()
    for a in r:
        print(a)

if __name__ == '__main__':
    main()
