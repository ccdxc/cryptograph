.. hazmat::

Bindings
========

.. toctree::
    :maxdepth: 1

    openssl
    interfaces


Getting a Backend Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: cryptography.hazmat.backends

``cryptography`` aims to support multiple backends to ensure it can provide
the widest number of supported cryptographic algorithms as well as supporting
platform specific implementations.

You can get the default backend by calling
:func:`~default_backend`.

The default backend will change over time as we implement new backends and
the libraries we use in those backends changes.


.. function:: default_backend()

    :returns: An object that provides at least
        :class:`~interfaces.CipherBackend`, :class:`~interfaces.HashBackend`, and
        :class:`~interfaces.HMACBackend`.

