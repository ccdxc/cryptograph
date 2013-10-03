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
Test using the NIST Test Vectors
"""

from __future__ import absolute_import, division, print_function

import binascii
import itertools
import os

import pytest

from cryptography.primitives.block import BlockCipher, ciphers, modes

from ..utils import load_nist_vectors_from_file


def parameterize_encrypt_test(cipher, vector_type, params, fnames):
    return pytest.mark.parametrize(params,
        list(itertools.chain.from_iterable(
            load_nist_vectors_from_file(
                os.path.join(cipher, vector_type, fname),
                "ENCRYPT",
                params
            )
            for fname in fnames
        ))
    )


class TestAES_CBC(object):
    @parameterize_encrypt_test(
        "AES", "KAT",
        ("key", "iv", "plaintext", "ciphertext"),
        [
            "CBCGFSbox128.rsp",
            "CBCGFSbox192.rsp",
            "CBCGFSbox256.rsp",
            "CBCKeySbox128.rsp",
            "CBCKeySbox192.rsp",
            "CBCKeySbox256.rsp",
            "CBCVarKey128.rsp",
            "CBCVarKey192.rsp",
            "CBCVarKey256.rsp",
            "CBCVarTxt128.rsp",
            "CBCVarTxt192.rsp",
            "CBCVarTxt256.rsp",
        ]
    )
    def test_KAT(self, key, iv, plaintext, ciphertext, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(key)),
            modes.CBC(binascii.unhexlify(iv)),
            api
        )
        actual_ciphertext = cipher.encrypt(binascii.unhexlify(plaintext))
        actual_ciphertext += cipher.finalize()
        assert binascii.hexlify(actual_ciphertext) == ciphertext

    @parameterize_encrypt_test(
        "AES", "MMT",
        ("key", "iv", "plaintext", "ciphertext"),
        [
            "CBCMMT128.rsp",
            "CBCMMT192.rsp",
            "CBCMMT256.rsp",
        ]
    )
    def test_MMT(self, key, iv, plaintext, ciphertext, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(key)),
            modes.CBC(binascii.unhexlify(iv)),
            api
        )
        actual_ciphertext = cipher.encrypt(binascii.unhexlify(plaintext))
        actual_ciphertext += cipher.finalize()
        assert binascii.hexlify(actual_ciphertext) == ciphertext


class TestAES_ECB(object):
    @parameterize_encrypt_test(
        "AES", "KAT",
        ("key", "plaintext", "ciphertext"),
        [
            "ECBGFSbox128.rsp",
            "ECBGFSbox192.rsp",
            "ECBGFSbox256.rsp",
            "ECBKeySbox128.rsp",
            "ECBKeySbox192.rsp",
            "ECBKeySbox256.rsp",
            "ECBVarKey128.rsp",
            "ECBVarKey192.rsp",
            "ECBVarKey256.rsp",
            "ECBVarTxt128.rsp",
            "ECBVarTxt192.rsp",
            "ECBVarTxt256.rsp",
        ]
    )
    def test_KAT(self, key, plaintext, ciphertext, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(key)),
            modes.ECB(),
            api
        )
        actual_ciphertext = cipher.encrypt(binascii.unhexlify(plaintext))
        actual_ciphertext += cipher.finalize()
        assert binascii.hexlify(actual_ciphertext) == ciphertext

    @parameterize_encrypt_test(
        "AES", "MMT",
        ("key", "plaintext", "ciphertext"),
        [
            "ECBMMT128.rsp",
            "ECBMMT192.rsp",
            "ECBMMT256.rsp",
        ]
    )
    def test_MMT(self, key, plaintext, ciphertext, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(key)),
            modes.ECB(),
            api
        )
        actual_ciphertext = cipher.encrypt(binascii.unhexlify(plaintext))
        actual_ciphertext += cipher.finalize()
        assert binascii.hexlify(actual_ciphertext) == ciphertext


class TestAES_OFB(object):
    @parameterize_encrypt_test(
        "AES", "KAT",
        ("key", "iv", "plaintext", "ciphertext"),
        [
            "OFBGFSbox128.rsp",
            "OFBGFSbox192.rsp",
            "OFBGFSbox256.rsp",
            "OFBKeySbox128.rsp",
            "OFBKeySbox192.rsp",
            "OFBKeySbox256.rsp",
            "OFBVarKey128.rsp",
            "OFBVarKey192.rsp",
            "OFBVarKey256.rsp",
            "OFBVarTxt128.rsp",
            "OFBVarTxt192.rsp",
            "OFBVarTxt256.rsp",
        ]
    )
    def test_KAT(self, key, iv, plaintext, ciphertext, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(key)),
            modes.OFB(binascii.unhexlify(iv)),
            api
        )
        actual_ciphertext = cipher.encrypt(binascii.unhexlify(plaintext))
        actual_ciphertext += cipher.finalize()
        assert binascii.hexlify(actual_ciphertext) == ciphertext

    @parameterize_encrypt_test(
        "AES", "MMT",
        ("key", "iv", "plaintext", "ciphertext"),
        [
            "OFBMMT128.rsp",
            "OFBMMT192.rsp",
            "OFBMMT256.rsp",
        ]
    )
    def test_MMT(self, key, iv, plaintext, ciphertext, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(key)),
            modes.OFB(binascii.unhexlify(iv)),
            api
        )
        actual_ciphertext = cipher.encrypt(binascii.unhexlify(plaintext))
        actual_ciphertext += cipher.finalize()
        assert binascii.hexlify(actual_ciphertext) == ciphertext


class TestAES_CFB(object):
    @parameterize_encrypt_test(
        "AES", "KAT",
        ("key", "iv", "plaintext", "ciphertext"),
        [
            "CFB128GFSbox128.rsp",
            "CFB128GFSbox192.rsp",
            "CFB128GFSbox256.rsp",
            "CFB128KeySbox128.rsp",
            "CFB128KeySbox192.rsp",
            "CFB128KeySbox256.rsp",
            "CFB128VarKey128.rsp",
            "CFB128VarKey192.rsp",
            "CFB128VarKey256.rsp",
            "CFB128VarTxt128.rsp",
            "CFB128VarTxt192.rsp",
            "CFB128VarTxt256.rsp",
        ]
    )
    def test_KAT(self, key, iv, plaintext, ciphertext, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(key)),
            modes.CFB(binascii.unhexlify(iv)),
            api
        )
        actual_ciphertext = cipher.encrypt(binascii.unhexlify(plaintext))
        actual_ciphertext += cipher.finalize()
        assert binascii.hexlify(actual_ciphertext) == ciphertext

    @parameterize_encrypt_test(
        "AES", "MMT",
        ("key", "iv", "plaintext", "ciphertext"),
        [
            "CFB128MMT128.rsp",
            "CFB128MMT192.rsp",
            "CFB128MMT256.rsp",
        ]
    )
    def test_MMT(self, key, iv, plaintext, ciphertext, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(key)),
            modes.CFB(binascii.unhexlify(iv)),
            api
        )
        actual_ciphertext = cipher.encrypt(binascii.unhexlify(plaintext))
        actual_ciphertext += cipher.finalize()
        assert binascii.hexlify(actual_ciphertext) == ciphertext
