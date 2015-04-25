a small and simple language wihtin project
`sblog <https://github.com/haoxun/sblog>`__.

Concepts
========

``sdataflow`` provides:

-  A small and simple language to define the relation of entries. An
   ``entry`` is a logic unit defined by user(i.e. a data processing
   function), it generates some kind of ``outcome`` as a respond to some
   kind of input ``outcome``\ (which might be genreated by other entry).
   All relations of a entry set forms a ``dataflow``.
-  A scheduler automatically runs entries and ships outcome to its
   destination.

Language
========

Tutorial
--------

Let's start with a simplest case(\ **one-to-one** relation):

::

    A --> B

where entry ``B`` accepts outcome of ``A`` as its input.

To define a **one-to-more** or **more-to-one** relation:

::

    # one-to-more
    A --> B
    A --> C
    A --> D

    # more-to-one
    B --> A
    C --> A
    D --> A

where in the **one-to-more** case, copies of outcome of ``A`` could be
passed to ``B``, ``C`` and ``D``. In the **more-to-one** case, outcomes
of ``B``, ``C`` and ``D`` would be passed to ``A``.

And here's the form of **outcome dispatching**, that is, a machanism of
sending different kinds of outcome of an entry to different
destinations. For instance, entry ``A`` genreates two kinds of outcome,
say ``[type1]`` and ``[type2]``, and pass outcomes of ``[type1]`` to
``B``, outcomes of ``[type2]`` to ``C``:

::

    # one way.
    A --> [type1]
    A --> [type2]
    [type1] --> B
    [type2] --> C

    # another way.
    A --[type1]--> B
    A --[type2]--> C

    # one-to-more example.
    A --> [type1]
    A --> [type2]
    [type1] --> B
    [type1] --> C
    [type2] --> D
    [type2] --> E

    # more-to-one example.
    A --> [type1]
    B --> [type1]
    [type1] --> C

where identifier embraced in brackets(i.e. ``[type1]``) represents the
type of outcome. In contrast to outcome dispatching, ``A --> B`` would
simple pass outcome of ``A``, with default type ``A``\ (the name of
entry generates the outcome), to ``B``. Essentially, above
form(statement contains brackets) overrides the type of outcome, and
acts like a filter for outcome dispatching.

After laoding all user defined dataflow, there are several steps of
analysis will be applied to such dataflow:

1. Build a DAG for dataflow. Break if error happens(i.e. syntax error,
   cyclic path).
2. Apply topology sort to DAG to get the order of entry invocation.

Lexical Rules
-------------

::

    ARROW          : re.escape('-->')
    DOUBLE_HYPHENS : re.escape('--')
    BRACKET_LEFT   : re.escape('[')
    BRACKET_RIGHT  : re.escape(']')
    ID             : r'\w+'

The effect of above rules would be equivalent as if passing such rules
to Python's ``re`` module with the flag ``UNICODE`` being set.

CFGs
----

::

    start : stats

    stats : stats single_stat
          | empty
          
    single_stat : entry_to_entry
                | entry_to_outcome_type
                | outcome_type_to_entry
                
    entry_to_entry : ID general_arrow ID

    general_arrow : ARROW
                  | DOUBLE_HYPHENS outcome_type ARROW

    outcome_type : BRACKET_LEFT ID BRACKET_RIGHT
                  
    entry_to_outcome_type : ID ARROW outcome_type

    outcome_type_to_entry : outcome_type ARROW ID

API
===

Form of Callback
----------------

As mentioned above, an entry stands for a user defined logic unit.
Hence, after defining the relations of entries with the language
discussed aboved, user should defines a set of callbacks, corrensponding
to each entry in the definition.

User can define two types of callback:

1. A **normal function** returns ``None``\ (i.e. a function with no
   ``return`` statement), or an iterable object, of which the element is
   a (key, value) tuple, with key as the name of outcome type and value
   as user defined object.
2. A generator yield the element same as (1).

Input argument list of both types of callback could be:

1. An empty list, meaning that such callback accept no data.
2. An one-element list.

Code fragment for illustration:

.. code:: python

    # normal function returns `None`, with empty argument list.
    def func1():
        pass


    # normal function return `None`, with one-element argument list.
    def func2(items):
        for name_of_outcome_type, obj in items:
            # do something.


    # normal function return elements, with one-element argument list.
    def func3(items):
        # ignore `items`
        data = [('some outcome type', i) for i in range(10)]
        return data


    # generator yield element, with one-element argument list.
    def gen1(items):
        # ignore `items`
        for i in range(10):
            yield 'some outcome type', i

Note that the name of outcome type is the string embraced in
brackets(\ **not** including the brackets).

Register Callback
-----------------

``sdataflow`` provides a class ``DataflowHandler`` to parse ``doc``\ (a
string represents the relations of entries), register callbacks and
schedule the execution of callbacks.

::

    class DataflowHandler
        __init__(self, doc, name_callback_mapping)
            `doc`: unicode or utf-8 encoded binary data.
            `name_callback_mapping`: a dict of (`name`, `callback`) pairs. `name`
            could be unicode or utf-8 encoded binary data. `callback` is a function
            or generator.
        
        run(self)
            Automatically execute all registered callbacks.

Example:

.. code:: python

    from sdataflow import DataflowHandler, create_data_wrapper

    doc = ('A --[odd]--> B '
           'A --[even]--> C '
           'B --> D '
           'C --> D ')

    def a():
        odd = create_data_wrapper('odd')
        even = create_data_wrapper('even')
        for i in range(1, 10):
            if i % 2 == 0:
                yield even(i)
            else:
                yield odd(i)

    def b(items):
        default = create_data_wrapper('B')
        # remove 1.
        for outcome_name, number in items:
            if number == 1:
                continue
            yield default(number)

    def c(items):
        default = create_data_wrapper('C')
        # remove 2.
        for outcome_name, number in items:
            if number == 2:
                continue
            yield default(number)

    def d(items):
        numbers = {i for _, i in items}
        assert set(range(3, 10)) == numbers

    name_callback_mapping = {
        'A': a,
        'B': b,
        'C': c,
        'D': d,
    }

    # parse `doc`, register `a`, `b`, `c`, `d`.
    handler = DataflowHandler(doc, name_callback_mapping)

    # execute callbacks.
    handler.run()

In above example, ``A`` generates numbers in the range of 1 to 9, of
which the odd numbers(1, 3, 5, 7, 9) are sent to ``B``, the even
numbers(2, 4, 6, 8) are sent to ``C``. Then ``B`` removes number 1 and
sends the rest(3, 5, 7, 9) to ``D``, while ``C`` removes number 2 and
sends the rest(4, 6, 8) to ``D``. Finally, ``D`` receives outcomes of
both ``C`` and ``D``, and make sure that is equal to
``set(range(3, 10))``.
