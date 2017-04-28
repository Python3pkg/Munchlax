Munchlax Data Objects
=====================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Munchlax data objects such as ``munchlax.lib.Message`` and ``munchlax.lib.Channel`` are wrappers
around Slack response objects. They have methods that allow you to more easily interact with them.

For example, to reply to a message all you need to do is call ``Message#reply``.

Munchlax data objects have attributes for all parts of a Slack response. If you want to get a message's
author's user ID, just use ``Message.user``. If you want to get the ``User`` object for a message's author
just call ``Message#get_author``.

A Note On Mutations
-------------------

Mutations on objects like channels will not be reflected by Munchlax data objects. If you do something like
``Channel#rename`` the ``Channel`` object will not automatically be updated. You will need to call ``Channel#update``.
It should be noted that not all objects have update methods. Messages in particular do not have update objects.
If you want to fetch an updated version of a message, you will need to do something like the following:

.. code-block:: python

    channel = await message.get_channel()
    updated_message = await channel.get_history(latest=message.ts, count=1)