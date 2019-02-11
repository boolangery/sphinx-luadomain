##########
sphinx-lua
##########

A sphinx lua domain.

Full example:

```rest
.. lua:alias:: Packet = table<string, number>

   A type alias.


.. lua:class:: Base

    A base class
    
    .. lua:attribute:: clsName: string

        The class name


.. lua:class:: Foo: Base

    My super lua class.

    .. lua:method:: append(i)
        :virtual:

        A virtual method.

        :param i: Value to append
        :type i: integer or None

    .. lua:staticmethod:: static(i)

        A static method.


    .. lua:method:: send(packet)
        :abstract:

        An abstract method.

        :param Packet packet: foo


.. py:function:: send(msg)

   Send a message to a recipient

   :param str packet: The person sending the message
   :type packet: string
   :return: the message id
   :rtype: int
```
