#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode:python -*-
# Filename: markdown.py
# Author:   Chenbin
# Time-stamp: <2017-04-12 Wed 23:17:12>


class Markdown(object):
    pass


class Content(Markdown):
    def __init__(self, *contents):
        self.contents = []
        self.contents.extend(contents)

    def __str__(self):
        return ''.join([str(x) for x in self.contents])


class Raw(Markdown):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return str(self.content)


class Title(Markdown):
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


class Division(Markdown):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '<div>{}</div>'.format(self.content)


class Separation(Markdown):
    def __init__(self):
        pass

    def __str__(self):
        return '<hr>'


class Strong(Markdown):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '<strong>{}</strong>'.format(self.content)


class Emphasis(Markdown):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '<em>{}</em>'.format(self.content)


class ListItems(Markdown):
    def __init__(self, ordered, *lists):
        self.lists = []
        self.lists.extend(lists)
        self.ordered = ordered

    def __str__(self):
        content = ''.join(['<li>{}</li>'.format(x) for x in self.lists])
        flag = 'ol' if self.ordered else 'ul'
        return '<{flag}>{content}</{flag}>'.format(flag=flag, content=content)


class Link(Markdown):
    def __init__(self, url, name=''):
        self.url = url
        self.name = name

    def __str__(self):
        return '<a href="{url}">{name}</a>'.format(url=self.url,
                                                   name=self.name)


class ImageLink(Link):
    def __str__(self):
        return '<img src="{url}">'.format(url=self.url)


class Break(Markdown):
    def __init__(self):
        pass

    def __str__(self):
        return '<br>'


class Code(Markdown):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return '<pre>{}</pre>'.format(self.code)
