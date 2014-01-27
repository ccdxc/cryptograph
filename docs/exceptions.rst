Exceptions
==========

.. currentmodule:: cryptography.exceptions

.. class:: AlreadyFinalized

    This is raised when a context is used after being finalized.


.. class:: InvalidSignature

    This is raised when the verify method of a hash context does not
    compare equal.


.. class:: NotYetFinalized

    This is raised when the AEAD tag property is accessed on a context
    before it is finalized.


.. class:: AlreadyUpdated

    This is raised when additional data is added to a context after update
    has already been called.


.. class:: UnsupportedAlgorithm

    This is raised when a backend doesn't support the requested algorithm (or
    combination of algorithms).


.. class:: InvalidKey

    This is raised when the verify method of a key derivation function does not
    compare equal.
