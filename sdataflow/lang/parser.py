# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from ply.yacc import yacc
from sdataflow.shared import Entry, OutcomeType
from .lexer import tokens as lexer_tokens


__all__ = ['create_parser']


tokens = lexer_tokens


# Following CFGs would simply tranform user defined dataflow into a series of
# 2-tuples. There are three kinds of 2-tuple:
#   * (Entry, OutcomeType), equivalent to `Entry --> [OutcomeType]`.
#   * (OutcomeType, Entry), equivalent to `[OutcomeType] --> Entry`.
#   * (Entry, Entry), equivalent to 'Entry --> Entry`.


def add_stat(stats, stat):
    # `stat` could be a 2-tuple, or a LIST of 2-tuples.
    if isinstance(stat, list):
        stats.extend(stat)
    else:
        stats.append(stat)


def p_stats(p):
    '''stats : stats single_stat
             | single_stat'''
    if len(p) == 3:
        add_stat(p[1], p[2])
        p[0] = p[1]
    else:
        p[0] = []
        add_stat(p[0], p[1])


def p_single_stat(p):
    '''single_stat : entry_to_entry
                   | entry_to_outcome_type
                   | outcome_type_to_entry'''
    p[0] = p[1]


def p_entry_to_entry(p):
    '''entry_to_entry : ID general_arrow ID'''
    if p[2] is None:
        # `A --> B`.
        p[0] = (Entry(p[1]), Entry(p[3]))
    else:
        # `A --[type]--> B`.
        p[0] = [
            (Entry(p[1]), p[2]),  # `A --> [type]`.
            (p[2], Entry(p[3])),  # `[type] --> B`.
        ]


def p_general_arrow(p):
    '''general_arrow : ARROW
                     | DOUBLE_HYPHENS outcome_type ARROW'''
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = p[2]


def p_outcome_type(p):
    '''outcome_type : BRACKET_LEFT ID BRACKET_RIGHT'''
    p[0] = OutcomeType(p[2])


def p_entry_to_outcome_type(p):
    '''entry_to_outcome_type : ID ARROW outcome_type'''
    p[0] = (Entry(p[1]), p[3])


def p_outcome_type_to_entry(p):
    '''outcome_type_to_entry : outcome_type ARROW ID'''
    p[0] = (p[1], Entry(p[3]))


def p_error(p):
    if p is None:
        # EOF.
        return
    print("Parser Error.")


def create_parser():
    return yacc(
        debug=0,
        optimize=1,
        tabmodule='generated_parsetab',
        outputdir=os.path.dirname(__file__),
    )
