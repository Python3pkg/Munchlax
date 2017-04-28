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