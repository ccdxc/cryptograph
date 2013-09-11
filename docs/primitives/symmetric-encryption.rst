Symmetric Encryption
====================

.. testsetup::

    import binascii
    key = binascii.unhexlify(b"0" * 32)
    iv = binascii.unhexlify(b"0" * 32)


Symmetric encryption is a way to encrypt (hide the plaintext value) material
where the encrypter and decrypter both use the same key.

.. class:: cryptography.primitives.block.BlockCipher(cipher, mode)

    Block ciphers work by encrypting content in chunks, often 64- or 128-bits.
    They combine an underlying algorithm (such as AES), with a mode (such as
    CBC, CTR, or GCM). A simple example of encrypting content with AES is:

    .. doctest::

        >>> from cryptography.primitives.block import BlockCipher, ciphers, modes
        >>> cipher = BlockCipher(ciphers.AES(key), modes.CBC(iv))
        >>> cipher.encrypt(b"a secret message") + cipher.finalize()
        '...'

    :param cipher: One of the ciphers described below.
    :param mode: One of the modes described below.

    ``encrypt()`` should be called repeatedly with new plaintext, and once the
    full plaintext is fed in, ``finalize()`` should be called.

    .. method:: encrypt(plaintext)

        :param bytes plaintext: The text you wish to encrypt.
        :return bytes: Returns the ciphertext that was added.

    .. method:: finalize()

        :return bytes: Returns the remainder of the ciphertext.

Ciphers
~~~~~~~

.. class:: cryptography.primitives.block.ciphers.AES(key)

    AES (Advanced Encryption Standard) is a block cipher standardized by NIST.
    AES is both fast, and cryptographically strong. It is a good default
    choice for encryption.

    :param bytes key: The secret key, either ``128``, ``192``, or ``256`` bits.
                      This must be kept secret.


Modes
~~~~~

.. class:: cryptography.primitives.block.modes.CBC(initialization_vector)

    CBC (Cipher block chaining) is a mode of operation for block ciphers. It is
    considered cryptographically strong.

    :param bytes initialization_vector: Must be random bytes. They do not need
                                        to be kept secret (they can be included
                                        in a transmitted message). Must be the
                                        same number of bytes as the
                                        ``block_size`` of the cipher. Do not
                                        reuse an ``initialization_vector`` with
                                        a given ``key``.

.. class:: cryptography.primitives.block.modes.OFB(nonce)

    OFB (Output Feedback) is a mode of operation for block ciphers. It
    transforms a block cipher into a stream cipher.

    :param bytes nonce: Must be random bytes. They do not need to be kept
                        secret (they can be included in a transmitted message).
                        Must be the same number of bytes as the ``block_size``
                        of the cipher.  Reuse of a ``nonce`` with a given
                        ``key`` can allow recovery of the original plaintext.

.. class:: cryptography.primitives.block.modes.CFB(initialization_vector)

    CFB (Cipher Feedback) is a mode of operation for block ciphers. It
    transforms a block cipher into a stream cipher.

    :param bytes initialization_vector: Must be random bytes. They do not need
                                        to be kept secret (they can be included
                                        in a transmitted message). Must be the
                                        same number of bytes as the
                                        ``block_size`` of the cipher. Do not
                                        reuse an ``initialization_vector`` with
                                        a given ``key``.


Insecure Modes
--------------

.. warning::

    These modes are insecure. New applications should never make use of them,
    and existing applications should strongly consider migrating away.


.. class:: cryptography.primitives.block.modes.ECB()

    ECB (Electronic Code Book) is the simplest mode of operation for block
    ciphers. Each block of data is encrypted in the same way. This means
    identical plaintext blocks will always result in identical ciphertext
    blocks, and thus result in information leakage
