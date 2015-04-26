# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from ply.yacc import yacc
from sdataflow.shared import Entity, Outcome
from .lexer import tokens as lexer_tokens


__all__ = ['create_parser']


tokens = lexer_tokens


# Following CFGs would simply tranform user defined dataflow into a series of
# 2-tuples. There are three kinds of 2-tuple:
#   * (Entity, Outcome), equivalent to `Entity --> [Outcome]`.
#   * (Outcome, Entity), equivalent to `[Outcome] --> Entity`.
#   * (Entity, Entity), equivalent to 'Entity --> Entity`.


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
    '''single_stat : entity_to_entity
                   | entity_to_outcome
                   | outcome_to_entity'''
    p[0] = p[1]


def p_entity_to_entity(p):
    '''entity_to_entity : ID general_arrow ID'''
    if p[2] is None:
        # `A --> B`.
        p[0] = (Entity(p[1]), Entity(p[3]))
    else:
        # `A --[type]--> B`.
        p[0] = [
            (Entity(p[1]), p[2]),  # `A --> [type]`.
            (p[2], Entity(p[3])),  # `[type] --> B`.
        ]


def p_general_arrow(p):
    '''general_arrow : ARROW
                     | DOUBLE_HYPHENS outcome ARROW'''
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = p[2]


def p_outcome(p):
    '''outcome : BRACKET_LEFT ID BRACKET_RIGHT'''
    p[0] = Outcome(p[2])


def p_entity_to_outcome(p):
    '''entity_to_outcome : ID ARROW outcome'''
    p[0] = (Entity(p[1]), p[3])


def p_outcome_to_entity(p):
    '''outcome_to_entity : outcome ARROW ID'''
    p[0] = (p[1], Entity(p[3]))


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
