Lua domain core-feature fixtures
=================================

.. The class/method/staticmethod/inheritance/alias/module/function examples
   below are the project's own documented examples, copied verbatim from
   README.rst, plus a few additions (data/classmethod/exception/
   currentmodule) to cover directives the README doesn't demonstrate.

.. lua:class:: pl.List

    Python-style list class.

    .. lua:attribute:: size: number

        The list size.

    .. lua:method:: append(elem)

        :param elem: The element to append
        :type elem: any

    .. lua:staticmethod:: fromArray(a) -> pl.List

        Create a List from a raw array.

        :return: The new List
        :rtype: pl.List

    .. lua:classmethod:: default() -> pl.List

        Return a shared default instance.

        :return: the default list
        :rtype: pl.List


.. lua:class:: ITransport

    .. lua:method:: startEngine() -> boolean
        :virtual:

        :return: true if engine started
        :rtype: boolean


.. lua:class:: Car: ITransport

    .. lua:method:: startEngine() -> boolean

        :return: true if engine started
        :rtype: boolean


.. lua:method:: foo()
    :virtual:
    :abstract:
    :deprecated:
    :protected:

    Show method modifiers.


.. lua:module:: pl.path

.. lua:function:: join(p1, p2) -> str

    Return the path resulting from combining the individual paths.

    :param p1: First path
    :type p1: str
    :param p2: An other path
    :type p2: str
    :return: The combined path
    :rtype: str

.. lua:data:: sep

    The platform's path separator.

.. lua:currentmodule:: pl.dir

.. lua:function:: makepath(p)

    Create a directory path.

    :param p: the path to create
    :type p: str

.. lua:currentmodule:: None

.. lua:exception:: PathError

    Raised on invalid path operations.


.. lua:alias:: Packet = table<string, number>

   A packet.


.. lua:class:: MessageSender

    A message sender.

    .. lua:method:: send(packet)
        :abstract:

        An abstract method.

        :param packet: the packet to send
        :type packet: Packet


Cross-references: :lua:class:`pl.List` and :lua:meth:`pl.List.append`.
