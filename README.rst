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

    ARROW             : re.escape('-->')
    TYPED_ARROW_LEFT  : re.escape('--')
    TYPED_ARROW_RIGHT : re.escape('-->')
    ENTRY             : r'\w'
    OUTCOME_TYPE      : r'\[\w\]'

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
                
    entry_to_entry : ENTRY general_arrow ENTRY

    general_arrow : ARROW
                  | TYPED_ARROW_LEFT OUTCOME_TYPE TYPED_ARROW_RIGHT
                  
    entry_to_outcome_type : ENTRY ARROW OUTCOME_TYPE

    outcome_type_to_entry : OUTCOME_TYPE ARROW ENTRY

API
===

coming soon.
