# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test using the OpenSSL Test Vectors
"""

from __future__ import absolute_import, division, print_function

import binascii

from cryptography.primitives.block import ciphers, modes

from .utils import generate_encrypt_test
from ..utils import load_openssl_vectors_from_file


class TestCamelliaCBC(object):
    test_OpenSSL = generate_encrypt_test(
        load_openssl_vectors_from_file,
        "Camellia",
        ["camellia-cbc.txt"],
        lambda key, iv: ciphers.Camellia(binascii.unhexlify(key)),
        lambda key, iv: modes.CBC(binascii.unhexlify(iv)),
        only_if=lambda api: api.supports_cipher(
            ciphers.Camellia("\x00" * 16), modes.CBC("\x00" * 16)
        ),
        skip_message="Does not support Camellia CBC",
    )


class TestCamelliaOFB(object):
    test_OpenSSL = generate_encrypt_test(
        load_openssl_vectors_from_file,
        "Camellia",
        ["camellia-ofb.txt"],
        lambda key, iv: ciphers.Camellia(binascii.unhexlify(key)),
        lambda key, iv: modes.OFB(binascii.unhexlify(iv)),
        only_if=lambda api: api.supports_cipher(
            ciphers.Camellia("\x00" * 16), modes.OFB("\x00" * 16)
        ),
        skip_message="Does not support Camellia OFB",
    )


class TestCamelliaCFB(object):
    test_OpenSSL = generate_encrypt_test(
        load_openssl_vectors_from_file,
        "Camellia",
        ["camellia-cfb.txt"],
        lambda key, iv: ciphers.Camellia(binascii.unhexlify(key)),
        lambda key, iv: modes.CFB(binascii.unhexlify(iv)),
        only_if=lambda api: api.supports_cipher(
            ciphers.Camellia("\x00" * 16), modes.CFB("\x00" * 16)
        ),
        skip_message="Does not support Camellia CFB",
    )
