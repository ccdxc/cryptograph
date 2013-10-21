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

from __future__ import absolute_import, division, print_function

import binascii

import pretend
import pytest

from cryptography.primitives.block import BlockCipher, ciphers, modes
from cryptography.primitives.block.base import _Operation


class TestBlockCipher(object):
    def test_instantiate_without_api(self):
        BlockCipher(
            ciphers.AES(binascii.unhexlify(b"0" * 32)),
            modes.CBC(binascii.unhexlify(b"0" * 32))
        )

    def test_use_after_finalize(self, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(b"0" * 32)),
            modes.CBC(binascii.unhexlify(b"0" * 32)),
            api
        )
        cipher.encrypt(b"a" * 16)
        cipher.finalize()
        with pytest.raises(ValueError):
            cipher.encrypt(b"b" * 16)
        with pytest.raises(ValueError):
            cipher.finalize()

    def test_encrypt_with_invalid_operation(self, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(b"0" * 32)),
            modes.CBC(binascii.unhexlify(b"0" * 32)),
            api
        )
        cipher._operation = _Operation.decrypt

        with pytest.raises(ValueError):
            cipher.encrypt(b"b" * 16)

    def test_finalize_with_invalid_operation(self, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(b"0" * 32)),
            modes.CBC(binascii.unhexlify(b"0" * 32)),
            api
        )
        cipher._operation = pretend.stub(name="wat")

        with pytest.raises(ValueError):
            cipher.finalize()

    def test_unaligned_block_encryption(self, api):
        cipher = BlockCipher(
            ciphers.AES(binascii.unhexlify(b"0" * 32)),
            modes.ECB(),
            api
        )
        ct = cipher.encrypt(b"a" * 15)
        assert ct == b""
        ct += cipher.encrypt(b"a" * 65)
        assert len(ct) == 80
