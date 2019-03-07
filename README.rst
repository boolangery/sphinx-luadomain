###############################################################################
sphinxcontrib-luadomain
###############################################################################

.. image:: https://img.shields.io/pypi/v/sphinxcontrib-luadomain.svg
    :target: https://pypi.python.org/pypi/sphinxcontrib-luadomain/
.. image:: https://img.shields.io/pypi/pyversions/sphinxcontrib-luadomain.svg
    :target: https://pypi.python.org/pypi/sphinxcontrib-luadomain/

A sphinx lua domain.


Installation
===============================================================================

.. code-block:: bash

    $ pip install sphinxcontrib-luadomain


Sphinx integration
===============================================================================

Add the following to your conf.py:

.. code-block:: python

    extensions = ['sphinxcontrib.luadomain']



Available sphinx directives
===============================================================================

The following directives are available:


Documenting class
-------------------------------------------------------------------------------

.. code-block:: rst

    .. lua:class:: pl.List

        Python-style list class.

        .. lua:attribute:: size: number

            The list size.

        .. lua:method:: append(elem)

            :param elem: The element to append
            :type elem: any

        .. lua:staticmethod:: fromArray(a): pl.List

            Create a List from a raw array.

            :return: The new List
            :rtype: pl.List


Class handle inheritance:

.. code-block:: rst

    .. lua:class:: ITransport

        .. lua:method:: startEngine(): boolean
            :virtual:

            :return: true if engine started
            :rtype: boolean

    .. lua:class:: Car: ITransport

        .. lua:method:: startEngine(): boolean

            :return: true if engine started
            :rtype: boolean


Method modifiers
-------------------------------------------------------------------------------

.. code-block:: rst

    .. lua:method:: foo()
        :virtual:
        :abstract:
        :deprecated:
        :protected:

        Show method modifiers.

Documenting module
-------------------------------------------------------------------------------

.. code-block:: rst

    .. lua:module:: pl.path

    .. lua:function:: join(p1, p2)

        Return the path resulting from combining the individual paths.

        :param p1: First path
        :type p1: str
        :param p2: An other path
        :type p2: str
        :return: The combined path
        :rtype: str


Type alias
-------------------------------------------------------------------------------


.. code-block:: rst

    .. lua:alias:: Packet = table<string, number>

       A packet.


    .. lua:class:: MessageSender

        A message sender.

        .. lua:method:: send(packet)
            :abstract:

            An abstract method.

            :param packet: the packet to send
            :type packet: Packet
