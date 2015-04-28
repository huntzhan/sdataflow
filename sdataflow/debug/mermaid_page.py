# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from io import open
from sdataflow.shared import Entity, Outcome


MODE_DEFAULT = 0
MODE_OUTCOME_AS_LINK_TEXT = 1
MODE_IGNORE_OUTCOME = 2

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


def get_js():
    # load `mermaid.full.js`.
    file_path = os.path.join(
        os.path.dirname(__file__),
        'mermaid.full.js',
    )
    return open(file_path, encoding='utf-8').read()


def render_template(mermaid_full_js, statements):
    return HTML_TEMPLAGE.format(mermaid_full_js, os.linesep.join(statements))


class NameContainer(object):

    element_name_mapping = {}
    count = 1

    @classmethod
    def clear(cls):
        cls.count = 1
        cls.element_name_mapping.clear()

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


class MermaidPageGenerator(object):

    def __init__(self, linear_ordering):
        self.linear_ordering = linear_ordering
        self.modify_linear_ordering()
        self.statements = ['graph LR']

    def render_definition(self, element):
        name, value = NameContainer.get_name_value_pair(element)
        if isinstance(element, Entity):
            template = self.ENTITY_DEFINITION
        elif isinstance(element, Outcome):
            template = self.OUTCOME_DEFINITION
        return template.format(name, value)

    def generate_page(self):
        self.generate_definition()
        self.generate_link()
        mermaid_full_js = get_js()
        return render_template(mermaid_full_js, self.statements)

    def modify_linear_ordering(self):
        pass

    def generate_definition(self):
        raise RuntimeError('Base Class.')

    def generate_link(self):
        raise RuntimeError('Base Class.')


class DefaultMode(MermaidPageGenerator):
    ENTITY_DEFINITION = '{0}{{{1}}}'
    OUTCOME_DEFINITION = '{0}({1})'

    def render_link(self, src, dst):
        return '{0} --> {1}'.format(NameContainer.get_name(src),
                                    NameContainer.get_name(dst))

    def generate_definition(self):
        for element in self.linear_ordering:
            self.statements.append(self.render_definition(element))

    def generate_link(self):
        for src in self.linear_ordering:
            for dst in src.get_adjacent_vertices():
                self.statements.append(self.render_link(src, dst))


class OutcomeAsLinkTextMode(MermaidPageGenerator):
    ENTITY_DEFINITION = '{0}({1})'

    def modify_linear_ordering(self):
        self.linear_ordering = [e for e in self.linear_ordering
                                if isinstance(e, Entity)]

    def render_link(self, src_entity, outcome, dst_entity):
        return '{0} -->|{1}| {2}'.format(
            NameContainer.get_name(src_entity),
            outcome.name,
            NameContainer.get_name(dst_entity),
        )

    def generate_definition(self):
        for element in self.linear_ordering:
            self.statements.append(self.render_definition(element))

    def generate_link(self):
        for src_entity in self.linear_ordering:
            for outcome in src_entity.get_adjacent_vertices():
                for dst_entity in outcome.get_adjacent_vertices():
                    self.statements.append(
                        self.render_link(
                            src_entity,
                            outcome,
                            dst_entity
                        ),
                    )


class IgnoreOutcomeMode(OutcomeAsLinkTextMode):

    def render_link(self, src_entity, outcome, dst_entity):
        return '{0} --> {1}'.format(
            NameContainer.get_name(src_entity),
            NameContainer.get_name(dst_entity),
        )


def generate_mermaid_page(linear_ordering, mode):
    NameContainer.clear()
    if mode == MODE_DEFAULT:
        page_generator = DefaultMode(linear_ordering)
    elif mode == MODE_OUTCOME_AS_LINK_TEXT:
        page_generator = OutcomeAsLinkTextMode(linear_ordering)
    elif mode == MODE_IGNORE_OUTCOME:
        page_generator = IgnoreOutcomeMode(linear_ordering)
    else:
        raise RuntimeError('Wrong mode.')
    return page_generator.generate_page()
