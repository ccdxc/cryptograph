# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import absolute_import, division, print_function

import base64
import struct
import warnings

from cryptography import utils
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers


def load_pem_traditional_openssl_private_key(data, password, backend):
    warnings.warn(
        "load_pem_traditional_openssl_private_key is deprecated and will be "
        "removed in a future version, use load_pem_private_key instead.",
        utils.DeprecatedIn06,
        stacklevel=2
    )

    return backend.load_traditional_openssl_pem_private_key(
        data, password
    )


def load_pem_pkcs8_private_key(data, password, backend):
    warnings.warn(
        "load_pem_pkcs8_private_key is deprecated and will be removed in a "
        "future version, use load_pem_private_key instead.",
        utils.DeprecatedIn06,
        stacklevel=2
    )

    return backend.load_pkcs8_pem_private_key(data, password)


def load_pem_private_key(data, password, backend):
    return backend.load_pem_private_key(data, password)


def load_pem_public_key(data, backend):
    return backend.load_pem_public_key(data)


def load_ssh_public_key(data, backend):
    key_parts = data.split(b' ')

    if len(key_parts) != 2 and len(key_parts) != 3:
        raise ValueError(
            'Key is not in the proper format or contains extra data.')

    key_type = key_parts[0]
    key_body = key_parts[1]

    if not key_type.startswith(b'ssh-'):
        raise ValueError('SSH-formatted keys must begin with \'ssh-\'.')

    if not key_type.startswith(b'ssh-rsa'):
        raise UnsupportedAlgorithm('Only RSA keys are currently supported.')

    return _load_ssh_rsa_public_key(key_body, backend)


def _load_ssh_rsa_public_key(key_body, backend):
    data = base64.b64decode(key_body)

    key_type, rest = _read_next_string(data)
    e, rest = _read_next_mpint(rest)
    n, rest = _read_next_mpint(rest)

    if key_type != b'ssh-rsa':
        raise ValueError(
            'Key header and key body contain different key type values.')

    if rest:
        raise ValueError('Key body contains extra bytes.')

    return backend.load_rsa_public_numbers(RSAPublicNumbers(e, n))


def _read_next_string(data):
    """Retrieves the next RFC 4251 string value from the data."""
    str_len, = struct.unpack('>I', data[:4])
    return data[4:4 + str_len], data[4 + str_len:]


def _read_next_mpint(data):
    """
    Reads the next mpint from the data.

    Currently, all mpints are interpreted as unsigned.
    """
    mpint_data, rest = _read_next_string(data)

    return _int_from_bytes(mpint_data, byteorder='big', signed=False), rest


if hasattr(int, "from_bytes"):
    _int_from_bytes = int.from_bytes
else:
    def _int_from_bytes(data, byteorder, signed=False):
        assert byteorder == 'big'
        assert not signed

        if len(data) % 4 != 0:
            data = (b'\x00' * (4 - (len(data) % 4))) + data

        result = 0

        while len(data) > 0:
            digit, = struct.unpack('>I', data[:4])
            result = (result << 32) + digit
            data = data[4:]

        return result
