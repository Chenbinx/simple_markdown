#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode:python -*-
# Filename: markdown.py
# Author:   Chenbin
# Time-stamp: <2017-04-08 Sat 15:20:34>


class Content(object):
    def __init__(self, *contents):
        self.contents = []
        self.contents.extend(contents)

    def __str__(self):
        return ''.join(map(lambda x: str(x), self.contents))


class Raw(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return str(self.content)


class Title(object):
    def __init__(self, level, content):
        if level < 1:
            self.level = 1
        elif level > 6:
            self.level = 6
        else:
            self.level = level
        self.content = content

    def __str__(self):
        return '<h{level}>{content}</h{level}>'.format(
            level=self.level,
            content=self.content)


class Paragraph(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '<p>{}</p>'.format(self.content)


class Separation(object):
    def __init__(self):
        pass

    def __str__(self):
        return '<hr>'


class Strong(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '<strong>{}</strong>'.format(self.content)


class Emphasis(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '<em>{}</em>'.format(self.content)


class ListItems(object):
    def __init__(self, ordered, *lists):
        self.lists = []
        self.lists.extend(lists)
        self.ordered = ordered

    def __str__(self):
        c = ''.join(map(lambda x: '<li>{}</li>'.format(x), self.lists))
        flag = 'ol' if self.ordered else 'ul'
        return '<{flag}>{content}</{flag}>'.format(flag=flag, content=c)


class Link(object):
    def __init__(self, url, name=''):
        self.url = url
        self.name = name

    def __str__(self):
        return '<a href="{url}">{name}</a>'.format(url=self.url,
                                                   name=self.name)


class ImageLink(Link):
    def __str__(self):
        return '<img src="{url}">'.format(url=self.url)


class Code(object):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return '<code>{}</code>'.format(self.code)


def main():
    c = Content(Title(1, Content('hello ', Emphasis('world'))),
                ListItems(True, Content('chap', Strong('ter1')), 'chapter2'),
                Separation(),
                Paragraph('hello world contents\nhello this is html\n'),
                Separation(),
                Code('''
function test() {
    alert(12)
}'''
                ),
                ImageLink('fsm', 'http://10.74.120.140:8080/docs/notes/cdsp/images/flocker/converge_fsm.png')
    )
    print(c)


if __name__ == '__main__':
    main()
