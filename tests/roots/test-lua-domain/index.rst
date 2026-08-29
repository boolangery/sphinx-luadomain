Lua domain test fixtures
========================

.. Signatures and descriptions below are transcribed verbatim from the
   official Lua 5.4 Reference Manual (https://www.lua.org/manual/5.4/manual.html),
   copyright Lua.org, PUC-Rio, MIT-licensed. Only the "-> type, type" return
   annotations are this project's own signature convention, added to encode
   what the manual documents each function as returning.

.. lua:function:: string.find(s, pattern [, init [, plain]]) -> integer, integer

    Looks for the first match of pattern (see §6.4.1) in the string s.
    If it finds a match, then find returns the indices of s
    where this occurrence starts and ends; otherwise, it returns fail.

    :param s: the string
    :type s: string
    :param pattern: the pattern to search for
    :type pattern: string
    :return: the indices of s where this occurrence starts and ends
    :rtype: integer, integer

.. lua:function:: math.modf(x) -> number, number

    Returns the integral part of x and the fractional part of x.
    Its second result is always a float.

    :param x: the number to split
    :type x: number
    :return: the integral part and the fractional part of x
    :rtype: number, number

.. Metamethod names are from manual section 2.4, "Metatables and Metamethods".

.. lua:class:: Vector

    A simple vector type used to exercise the ``metamethod`` directive.

    .. lua:metamethod:: __add(other) -> Vector

        the addition (+) operation.

        :param other: the other operand
        :type other: Vector
        :return: the sum of the two vectors
        :rtype: Vector

    .. lua:metamethod:: __ad(other) -> Vector

        Deliberately misspelled metamethod name, to exercise the
        unknown-metamethod warning.
