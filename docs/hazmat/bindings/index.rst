.. hazmat::

Bindings
========

.. currentmodule:: cryptography.hazmat.bindings

``cryptography`` aims to provide low-level CFFI based bindings to multiple
native C libraries. These provide no automatic initialisation of the library
and may not provide complete wrappers for its API.

Using these functions directly is likely to require you to be careful in
managing memory allocation, locking and other resources.


Individual Bindings
-------------------

.. toctree::
    :maxdepth: 1

    openssl
