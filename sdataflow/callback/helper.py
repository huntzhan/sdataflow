# -*- coding: utf-8 -*-
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from sdataflow.shared import to_unicode


def create_data_wrapper(outcome_type_name):
    name = to_unicode(outcome_type_name)
    if name is None:
        raise RuntimeError('create_data_wrapper')

    def wrapper(data):
        return (outcome_type_name, data)

    return wrapper
