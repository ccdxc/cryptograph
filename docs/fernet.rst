Fernet
======

.. currentmodule:: cryptography.fernet

.. testsetup::

    import base64
    import binascii
    key = base64.urlsafe_b64encode(binascii.unhexlify(b"0" * 64))


`Fernet`_ is an implementation of symmetric (also known as "secret key")
authenticated cryptography. Fernet provides guarantees that a message encrypted
using it cannot be manipulated or read without the key.

.. class:: Fernet(key)

    This class provides both encryption and decryption facilities.

    .. doctest::

        >>> from cryptography.fernet import Fernet
        >>> f = Fernet(key)
        >>> ciphertext = f.encrypt(b"my deep dark secret")
        >>> ciphertext
        '...'
        >>> f.decrypt(ciphertext)
        'my deep dark secret'

    :param bytes key: A base64 encoded 32-byte key. This **must** be kept
                      secret. Anyone with this key is able to create and read
                      messages.


    .. method:: encrypt(plaintext)

        :param bytes plaintext: The message you would like to encrypt.
        :returns bytes: A secure message which cannot be read or altered
                        without the key. It is URL safe base64-encoded.

    .. method:: decrypt(ciphertext, ttl=None)

        :param bytes ciphertext: An encrypted message.
        :param int ttl: Optionally, the number of seconds old a message may be
                        for it to be valid. If the message is older than
                        ``ttl`` seconds (from the time it was originally
                        created) an exception will be raised. If ``ttl`` is not
                        provided (or is ``None``), the age of the message is
                        not considered.
        :returns bytes: The original plaintext.


.. _`Fernet`: https://github.com/fernet/spec/
