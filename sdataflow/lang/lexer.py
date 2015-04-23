# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import re
from ply.lex import TOKEN, lex


__all__ = ['create_lexer', 'tokens']


tokens = [
    'ARROW',
    'DOUBLE_HYPHENS',
    'BRACKET_LEFT',
    'BRACKET_RIGHT',
    'ID',
]

t_ARROW = re.escape('-->')
t_DOUBLE_HYPHENS = re.escape('--')
t_BRACKET_LEFT = re.escape('[')
t_BRACKET_RIGHT = re.escape(']')
t_ID = r'\w+'


# misc configurations.
t_ignore_COMMENT = r'\#.*'
t_ignore_WHITESPACE = r'\s'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Lexer Error: [{0}]{1}".format(t.value[0], t.value[1:]))
    t.lexer.skip(1)


def create_lexer():
    return lex(
        debug=0,
        optimize=1,
        lextab="generated_lextab",
        outputdir=os.path.dirname(__file__),
        reflags=re.UNICODE,
    )
