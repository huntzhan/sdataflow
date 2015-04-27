# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from io import open
from sdataflow.shared import Entity, Outcome


HTML_TEMPLAGE = '''
<html>
<head>
<script>
{0}
</script>
</head>
<body>
<div class="mermaid">
{1}
</div>
</body>
</html>
'''


class NameContainer(object):

    element_name_mapping = {}
    count = 1

    @classmethod
    def get_name(cls, element):
        if element not in cls.element_name_mapping:
            cls.element_name_mapping[element] = 'id' + str(cls.count)
            cls.count = cls.count + 1
        return cls.element_name_mapping[element]

    @classmethod
    def get_name_value_pair(cls, element):
        name = cls.get_name(element)
        if isinstance(element, Entity):
            value = 'Entity: {0}'.format(element.name)
        elif isinstance(element, Outcome):
            value = 'Outcome: {0}'.format(element.name)
        return name, value


def generate_definition(element):
    name, value = NameContainer.get_name_value_pair(element)
    if isinstance(element, Entity):
        return '{0}{{{1}}}'.format(name, value)
    elif isinstance(element, Outcome):
        return '{0}({1})'.format(name, value)


def generate_link(src, dst):
    return '{0} --> {1}'.format(NameContainer.get_name(src),
                                NameContainer.get_name(dst))


def get_js():
    # load `mermaid.full.js`.
    file_path = os.path.join(
        os.path.dirname(__file__),
        'mermaid.full.js',
    )
    return open(file_path, encoding='utf-8').read()


def render_template(mermaid_full_js, statements):
    return HTML_TEMPLAGE.format(mermaid_full_js, os.linesep.join(statements))


def generate_mermaid_page(linear_ordering):
    statements = ['graph LR']
    # definition.
    for element in linear_ordering:
        statements.append(generate_definition(element))
    # link.
    for src in linear_ordering:
        for dst in src.get_adjacent_vertices():
            statements.append(generate_link(src, dst))
    # page.
    mermaid_full_js = get_js()
    return render_template(mermaid_full_js, statements)
